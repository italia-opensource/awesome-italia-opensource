import React from 'react';
import Layout from '@theme/Layout';
import TableFeatures from '@site/src/components/TableFeatures';
import NewsletterForm from '@site/src/components/NewsletterForm';


export default function Home(): JSX.Element {
  return (
    <Layout
      title={`Home`}
      wrapperClassName="layout"
      description="Italia Opensource is a list of open source projects created by Italian companies or developers. The repository intends to give visibility to open source projects and stimulate the community to contribute to growing the ecosystem.">
      <main className="main">
        

        <section className="wrapper">
        <div className="content">

        <header>
              <h1>Italia Opensource</h1>
            </header>
            <section>
              <p>
                Italia Opensource is a list of open source projects created by Italian companies or developers.<br/>
                The repository intends to give visibility to open source projects and stimulate the community to contribute to growing the ecosystem.
              </p>
              <TableFeatures />
            </section>
          </div>

        </section>

        <section className="wrapper">
          <div className="content">
            <header>
              <h1>Subscribe Us</h1>
            </header>
            <section>
              <p>
              The newsletter will be dedicated to keeping you updated on new open source projects in the Italian community and events around the country.
              </p>
            </section>
            <footer>
              <NewsletterForm />
            </footer>
          </div>
        </section>
      </main>
    </Layout>
  );
}