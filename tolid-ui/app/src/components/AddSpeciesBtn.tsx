/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import GenericRequestBtn from "./GenericRequestBtn";

function AddSpeciesBtn() {
  return (
    <a href="/admin/add-species">
      <GenericRequestBtn
        variant="add"
        text="Add"
      />
    </a>
  )
}

export default AddSpeciesBtn;
