import React from "react";
import UserToLIDsList from "../components/profile/UserToLIDsList"
import UserRequestsList from "../components/profile/UserRequestsList"

function Profile() {
  return (
    <div className="contact">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">Profile</h1>
          </div>
        </div>
        <div className="bg-circle-1 bg-circle"></div>
        <div className="bg-circle-2 bg-circle"></div>
        <div className="bg-circle-3 bg-circle"></div>
        <div className="bg-circle-4 bg-circle"></div>
      </header>
      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12">
              <div className="p-5">
                <h2>My ToLIDs</h2>
                <UserToLIDsList />
                <h2>My Requests</h2>
                <UserRequestsList />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Profile;