import React from 'react';
import Layout from '@theme/Layout';
import TableFeatures from '@site/src/components/TableFeatures';


export default function Home(): JSX.Element {
  return (
    <Layout
      title={`Home`}
      description="Italia Opensource is a list of open source projects created by Italian companies or developers. The repository intends to give visibility to open source projects and stimulate the community to contribute to growing the ecosystem.">
      <main>
        <TableFeatures />
      </main>
    </Layout>
  );
}
