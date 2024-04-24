/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Header, HeaderButton } from '@tol/tol-ui';


const docs: HeaderButton = {
  href: "https://ssg-confluence.internal.sanger.ac.uk/display/TOL/ToL+UI+Library",
  text: "Documentation"
};

function Home() {
  return (
    <div className="home">
      <Header
        title="ToLID"
        subTitle="Tree of Life Identifiers"
        buttons={[docs]}
        pageEmpty
      />
    </div>
  );
}

export default Home;