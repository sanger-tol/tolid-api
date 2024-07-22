/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

interface Props {
    taxonId: string,
    requestedTaxonId: string
  }
  
  function SubspeciesCellRenderer(props: Props) {
    const { taxonId, requestedTaxonId } = props;
  
    return (
      <div>
        {taxonId}
        {String(requestedTaxonId) !== taxonId && (
          <p>Sub-speices: {requestedTaxonId}</p>
        )}
      </div>
    );
  }
  
  export default SubspeciesCellRenderer;
