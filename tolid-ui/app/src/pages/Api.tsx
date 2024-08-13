/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Widgets } from '@tol/tol-ui';


function Api() {
  const usingTheApi = (
    <div>
        <h2 className="sub-heading">Using the ToLID API</h2>
        <p className="text">It is possible to interact with the ToLID system via a REST API endpoint,
          requesting (and, if authorised, creating) ToLIDs. To get started, please <a href="mailto:tolid-help@sanger.ac.uk">email us</a> to
          request an API key.</p>
        <p className="text">The endpoint you'll use is <code>POST https://id.tol.sanger.ac.uk/api/v3/request/create</code>, posting a payload</p>
        <p><pre><code>
          {`[
  {
    "specimen_id": "ABC123",  // Your internal specimen ID
    "requested_taxonomy_id": 123456,  // species or sub-species taxonomy ID
    "confirmation_name": "Arenicola marina"  // optional
  }
]`}
        </code></pre></p>
        <p>and HTTP header <code>token: &lt;your-api-token&gt;</code>.</p>
        <p>Depending on your role, you'll receive a response as follows:</p>
        <h5>For a normal user</h5>
        <p><pre><code>
          {`{
  "data": [
    {
      "type": "request",
      "id": "request-id"
      // More stuff here
    }
  ]
}`}
        </code></pre></p>
        <p>The request will then be actioned by a curator, after which your assigned ToLID
          will appear on your website profile page.</p>
        <h5>For a "creator" user</h5>
        <p><pre><code>
          {`{
  "data": [
    {
      "type": "specimen",
      "id": "abCdeFghi1"
      // More stuff here
    }
  ]
}`}
        </code></pre></p>
        <p>Creators are able to create ToLIDs without them needing to be approved by a curator. If, however,
          a ToLID is requested for a species that is not in the database, this will need action by a curator
          so a <code>request</code> object will be returned on the endpoint. It is recommended to resend the request every
          24 hours until a <code>tolid</code> object is returned.</p>

          <h5>Testing your integration</h5>
          <p>We have a staging server on which you can test your integration before putting it into
            production: <code>https://id-staging.tol.sanger.ac.uk/api/v3/request/create</code>. The API key is the same as the production server.
            Please do not use any ToLIDs given out by the staging server as they may be different to what you get from the production
            server!</p>

      </div>
  );
  
  const components = [
    {
      component: usingTheApi,
      type: 'full'
    }
  ];

  return (
    <div className="api">
      <Widgets
        components={components}
      />
    </div>
  );
}

export default Api;