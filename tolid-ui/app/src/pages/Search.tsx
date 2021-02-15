import React from "react";
import SearchResults from "../components/search/SearchResults"

function Search() {
  return (
    <div className="search">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">Search</h1>
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
            <div className="col-lg-12 order-lg-1">
                <SearchResults/>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Search;