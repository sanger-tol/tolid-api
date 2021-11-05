{/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/}

import * as React from 'react';
import { ErrorMessage } from '../../models/ErrorMessage'
import { httpClient } from '../../services/http/httpClient';
import { Modal } from "react-bootstrap";

import './RequestsList.scss'

export interface Props {
  show: boolean,
  toggle?: () => void,
  requestId: number
}
export interface State {
  error: ErrorMessage | null,
  message: string,
  customDisabled: boolean,
  rejectInput: string
}

class RejectModal extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      error: null,
      message: '',
      customDisabled: true,
      rejectInput: ""
    };
  }

  rejectRequest = (event: any) => {
    var rejectReason: string | null = null;
    if (this.state.rejectInput !== '') {
      rejectReason = this.state.rejectInput
    }

    httpClient().patch('requests/'+this.props.requestId+'/reject', null, { params: {reason: rejectReason} })
      .then(data => {
        this.setState({
          error: null,
          message: "Request "+data.data[0].requestId+" has been rejected"
        })
      })
      .catch((err: any) => {
        this.setState({
          error: err
        })
      })
      .finally(() => {
        if (this.props.toggle) {
          this.props.toggle();
        }
      })
  }

  disableCustomReason = (event: any) => {
    this.setState({
      customDisabled: true,
      rejectInput: event.target.value
    })
  }

  toggleCustomReason = (event: any) => {
    if (this.state.customDisabled === true) {
      this.setState({
        customDisabled: false,
      })
    }
    this.setState({
      rejectInput: event.target.value
    })
  }

  toggleHide = () => {
    if (this.props.toggle) {
      this.props.toggle()
    }
    this.setState ({
      rejectInput: "",
      customDisabled: true
    })
  }

  public render() {
    return (
      <div>
        <Modal 
          show={this.props.show}
          onHide={this.toggleHide}
          aria-labelledby="contained-modal-title-vcenter"
          centered
        >
          <Modal.Header>
            <h2>Reason for rejection (ID: {this.props.requestId})</h2>
          </Modal.Header>
          <Modal.Body>
            <p className="text-primary">* A rejection reason is not required</p>
            <div className="form-group">
              <form id="reject-form">
                <fieldset className="form-group">
                  <div className="row">
                    <legend className="col-form-label col-sm-2 pt-0">Reason:</legend> 
                    <div className="col-sm-10">
                      <div className="form-check">
                        <input className="form-check-input" type="radio" onChange={this.disableCustomReason} name="gridRadios" id="radio1" value="Taxonomy ID is not species-level"/>
                        <label htmlFor="radio1" className="form-check-label">
                          Taxonomy ID is not species-level
                        </label>
                      </div>
                      <div className="form-check">
                        <input className="form-check-input" type="radio" onChange={this.toggleCustomReason} name="gridRadios" id="custom" value=""/>
                        <label htmlFor="custom" className="form-check-label">
                          Custom:
                        </label>
                      </div>
                    </div>
                  </div>
                </fieldset>
                <div className="form-group row">
                <legend className="col-form-label col-sm-2 pt-0"/>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" onChange={this.toggleCustomReason} value={this.state.rejectInput} disabled={this.state.customDisabled}/>
                  </div>
                </div>
              </form>
            </div>
            <p className="text-danger">Note: The rejection reason is viewable by the requester!</p>
          </Modal.Body>
          <Modal.Footer>
            <button className="btn btn-sm btn-light" onClick={this.toggleHide}>Cancel</button>
            <button type="submit" form="reject-form" className="btn btn-sm btn-danger" onClick={this.rejectRequest}>Reject</button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}
  export default RejectModal;