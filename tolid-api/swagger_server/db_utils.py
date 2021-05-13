from swagger_server.model import db, TolidSpecies, TolidSpecimen, TolidRequest
from swagger_server.email_utils import MailUtils
import os


def create_new_specimen(species, specimen_id, user):
    highest = species.current_highest_tolid_number()
    number = highest + 1
    specimen = TolidSpecimen(specimen_id=specimen_id, number=number,
                             tolid=species.prefix+str(number))
    specimen.species = species
    specimen.user = user
    return specimen


def create_request(taxonomy_id, specimen_id, user):
    request = db.session.query(TolidRequest) \
        .filter(TolidRequest.specimen_id == specimen_id) \
        .filter(TolidRequest.species_id == taxonomy_id) \
        .one_or_none()
    if request is None:
        request = TolidRequest(specimen_id=specimen_id,
                               species_id=taxonomy_id,
                               status="Pre-pending")
        request.user = user
    else:
        if request.user != user:
            raise Exception("Another user has requested a ToLID for specimenId "
                            + specimen_id + " and taxonomyId " + str(taxonomy_id))
    return request


def accept_request(request):
    species = db.session.query(TolidSpecies) \
        .filter(TolidSpecies.taxonomy_id == request.species_id) \
        .one_or_none()
    if species is None:
        raise Exception("Species not in database")
    specimen = create_new_specimen(species, request.specimen_id, request.user)
    db.session.add(specimen)
    db.session.delete(request)
    db.session.commit()

    if specimen.user.email is not None and specimen.user.email.strip() != "":
        try:
            tolid_created_mail_template, subject = MailUtils.get_tolid_created(specimen)
            MailUtils.send(tolid_created_mail_template, subject,
                           specimen.user.email)
        except Exception:
            pass

    return specimen


def reject_request(request):
    request.status = "Rejected"
    db.session.commit()
    return request


def notify_requests_pending():
    requests = db.session.query(TolidRequest) \
        .filter(TolidRequest.status == "Pre-pending") \
        .all()
    if len(requests) > 0:
        # Send email notification
        try:
            requests_pending_mail_template, subject = MailUtils.get_requests_pending()
            MailUtils.send(requests_pending_mail_template, subject,
                           os.environ['MAIL_RECEIVER_REQUESTS_PENDING'])
        except Exception:
            pass
        # Set status to Pending
        for request in requests:
            request.status = "Pending"
