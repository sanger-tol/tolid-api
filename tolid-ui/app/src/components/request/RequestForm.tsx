import * as React from 'react';
import { Request } from '../../models/Request'
import { ErrorMessage } from '../../models/ErrorMessage'
import { httpClient } from '../../services/http/httpClient';

import './RequestForm.scss'

export interface Props {
}
export interface State {
    ret: Request | ErrorMessage | null,
}

function makeRequest(taxonomyId: number, specimenId: string): Promise<Request|ErrorMessage> {

  var postData = [{taxonomyId: taxonomyId, specimenId: specimenId}];
  return httpClient().post('/requests', postData)
    .then((data: any) => {
      return data.data[0] as Request       
    })
    .catch((err: any) => {
      return err as ErrorMessage
    })
}

class RequestForm extends React.Component<Props, State> {
    constructor(props: Props) {
      super(props);
      this.state = {
        ret: null
      }
    }

    sendRequest = (event: any) => {
        event.preventDefault();
        const form = document.getElementById("requestForm") as HTMLFormElement;
        const taxonomyId = document.getElementById("taxonomyId") as HTMLInputElement;
        const specimenId = document.getElementById("specimenId") as HTMLInputElement;

        // If our input has a value
        if ((taxonomyId.value !== "") && (specimenId.value !== "")) {
          makeRequest(parseInt(taxonomyId.value), specimenId.value)
            .then(request => this.setState({ ret: request }))
          // Finally, we need to reset the form
          taxonomyId.classList.remove("is-invalid");
          specimenId.classList.remove("is-invalid");
          form.reset();
        } else {
          // If the input doesn't have a value, make the border red since it's required
          taxonomyId.classList.add("is-invalid");
          specimenId.classList.add("is-invalid");
        }
    };

    public render() {
      return (
        <div>
            {(this.state.ret !== null) && ("detail" in this.state.ret) &&
            <p className="alert alert-danger">
                {this.state.ret.title}: {this.state.ret.detail}
            </p>
            }
            {(this.state.ret !== null) && ("requestId" in this.state.ret) &&
            <p className="alert alert-success">
                The ToLID has been requested. You'll be notified by email when allocated.
            </p>
            }

            <form className="form" id="requestForm">
                <div className="form-group">
                  <input type="text" className="form-control form-control-lg" id="taxonomyId" placeholder="NCBI Taxonomy ID" />
                  <small className="form-text text-muted">
                    The Taxonomy ID as registered at NCBI. This must be a species-level taxonomy ID.
                  </small>
                  <input type="text" className="form-control form-control-lg" id="specimenId" placeholder="Specimen ID" />
                  <small className="form-text text-muted">
                    The internal ID of the specimen. This is only used in the ToLID system and should be how you refer to the specimen in your lab
                  </small>
                </div>
                <button className="btn btn-primary" id="makeRequestButton" onClick={this.sendRequest}>
                Request
                </button>
            </form>
        </div>
      );
    }
  }
  export default RequestForm;