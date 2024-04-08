# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from sqlalchemy.orm import Session

from main.email_utils import MailUtils
from main.model import TolidRequest, TolidSpecies, TolidSpecimen, TolidUser


def create_new_specimen(species: TolidSpecies, specimen_id, user):
    highest = species.current_highest_tolid_number()
    number = highest + 1
    specimen = TolidSpecimen(specimen_id=specimen_id, number=number,
                             tolid=species.prefix + str(number))
    specimen.species = species
    specimen.user = user
    return specimen


def create_request(sess: Session, taxonomy_id, specimen_id, user, confirmation_name=None):
    request = sess.query(TolidRequest) \
        .filter(TolidRequest.specimen_id == specimen_id) \
        .filter(TolidRequest.species_id == taxonomy_id) \
        .one_or_none()
    if request is None:
        request = TolidRequest(specimen_id=specimen_id,
                               species_id=taxonomy_id,
                               status='Pre-pending',
                               confirmation_name=confirmation_name)
        request.user = user
    else:
        if request.user != user:
            raise Exception('Another user has requested a ToLID for specimenId '
                            f'{specimen_id} and taxonomyId {taxonomy_id}')
    return request


def accept_request(request, sess: Session):
    species = sess.query(TolidSpecies) \
        .filter(TolidSpecies.taxonomy_id == request.species_id) \
        .one_or_none()
    if species is None:
        raise Exception('Species not in database')
    specimen = create_new_specimen(species, request.specimen_id, request.user)
    sess.add(specimen)
    sess.delete(request)
    sess.commit()

    if specimen.user.email is not None and specimen.user.email.strip() != '':
        try:
            tolid_created_mail_template, subject = MailUtils.get_tolid_created(specimen)
            MailUtils.send(tolid_created_mail_template, subject,
                        specimen.user.email)
        except Exception:
            pass

    return specimen.to_dict()


def reject_request(request, reason, sess: Session):
    request.status = 'Rejected'
    if reason is not None:
        request.reason = reason
    sess.commit()

    user = sess.query(TolidUser) \
        .filter(request.created_by == TolidUser.user_id) \
        .one_or_none()

    if user.email is not None and user.email.strip() != '':
        try:
            tolid_created_mail_template, subject = MailUtils.get_tolid_rejected(request)
            MailUtils.send(tolid_created_mail_template, subject,
                           user.email)
        except Exception:
            pass

    return request


def notify_requests_pending(sess: Session):
    requests = sess.query(TolidRequest) \
        .filter(TolidRequest.status == 'Pre-pending') \
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
            request.status = 'Pending'
