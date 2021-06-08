import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">ToLID</h1>
            <h2 className="masthead-subheading mb-0">Tree of Life Identifiers</h2>
            <a href="api/v2/ui/" className="btn btn-primary btn-xl rounded-pill mt-5">Use the API</a>
            <Link to="/search" className="btn btn-primary btn-xl rounded-pill mt-5">Search</Link>
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
              <div className="p-5">
                <h2 className="display-4">What are ToLIDs?</h2>
                <p>A complete ToLID is a unique identifier for an individuum of a species sampled for genome sequencing and consists of</p>
                <ul>
                  <li>the ToLID prefix made up of
                    <ul>
                      <li>a lower case letter for the high level taxonomic rank and a lower case letter for the clade (see clade prefix assignments below). Only one letter is used for vertebrates (VGP legacy).</li>
                      <li>one upper, two lower case letters for genus</li>
                      <li>one upper, three lower case letters for species (one upper, two lower case for vertebrates, VGP legacy)</li>
                    </ul>
                  </li>
                  <li>a number to indicate the individual that was sampled. The number is assigned in order of request and does not represent any ranking.</li>
                </ul>
                <p>e.g. <strong>aRanTem1</strong> for the first sampled individual of Rana temporaria, <strong>xgPerPere3</strong> for the third sampled individual of Peregriana peregra</p>
                
                <p>For naming genome assemblies of samples, we recommend to use the full ToLID and add .&lt;version&gt;
                Examples:</p>
                <ul>
                  <li>fCotGob3.1 (first assembly version of the 3rd individual of Cottoperca gobio)</li>
                  <li>fAstCal1.2 (second assembly version of the first individual of Astatotilapia calliptera)</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12">
              <div className="p-5">
                <h2 className="display-4">Why do we need them?</h2>
                <p>ToLIDs add a unique, easy to communicate identifier that provides species recognition, differentiates between specimen of the same species and adds some taxonomic context.</p>
                <p>The <a href="https://www.earthbiogenome.org/">Earth BioGenome Project (EBP)</a> recommends that all samples to be sequenced are registered for a ToLID. This helps with your internal records, facilitates internal and external communication about the samples and helps the EBP tracking all sequencing projects.</p>
                <p>ToLIDs are not a competition or replacement for INSDC BioSample records which hold all the metadata associated with the sample. Every sample should have both.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12">
              <div className="p-5">
                <h2 className="display-4">How can I get one?</h2>
                <p>On this website is a self-service system to enable you to simply enter your sample’s taxonomy ID and any internal identifier (the latter so that we can spot it if you accidentally ask for a ToLID for the same sample again) and get a ToLID in return. Click on the Login button and log in using Elixir, then click on "Create". ToLIDs go through a manual acceptance process but we aim to create them within 48 hours of request.</p>
                <p>You can search for already assigned ToLIDs in the search box above. The API documentation for the ToLID database can be found <a href="/api/v2/ui">here</a>.</p>
                <p>Any problems, <a href="mailto:tolid-help@sanger.ac.uk">email us</a>.</p>
                </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12 order-lg-1">
              <div className="p-5">
                <h2 className="display-4">What if the species is missing in the ToLID database?</h2>
                <p>The ToLID database contains all British angiosperms (BotSocBritIsles), all valid British taxa with taxonomy (NHM) and all “species” with sequence in INSDC. If a species is not in the database yet we'll add it.</p>
                <p>A species needs to have a taxonomy ID before ToLIDs can be requested. If not present, these should be requested and obtained from taxonomyDB first before contacting us. Instructions can be found <a href="https://ena-docs.readthedocs.io/en/latest/faq/taxonomy_requests.html">here</a>.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12 order-lg-1">
              <div className="p-5">
                <h2 className="display-4">How did you make the ToLIDs?</h2>
                <p>The list of unique prefixes assigned to species in the ToLID API is maintained in <a href="https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming">GitLab repository</a>.</p>
                <p>In order to assign two-letter prefixes (the first part of a ToLID) to all life, we proposed a pragmatic hierarchical grouping with the first letter based on higher level groups and the second letter defining sub groups within them. For legacy reasons, vertebrates are prefixed with one letter only. Although standard high level names are used for many groups, these are at a variety of taxonomic ranks, and others designations involve clearly non-monophyletic groupings, including catch-all clusters such as for example "other-animal-phyla". This assignment achieves a practical and manageable grouping that has proven robust to working through large lists of species from multiple sources with often contradicting taxonomic data. The groups explicitly do not represent assertions about taxonomy in general or taxonomic assignment of individual species.</p>
                <table className="table table-striped">
                  <thead>
                    <tr>
                      <th>First prefix</th>
                      <th>Second prefix</th>
                      <th>Covers</th>
                      <th>Covers in detail</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>a</td><td></td><td>amphibia</td><td>Amphibia</td></tr>
                    <tr><td>b</td><td></td><td>birds</td><td>Aves</td></tr>
                    <tr><td>c</td><td>a</td><td>non-vascular plants</td><td>Andreaeopsida</td></tr>
                    <tr><td>c</td><td>b</td><td>non-vascular plants</td><td>Andreaeobryopsida, Bryopsida, Chlorokybophyceae, Oedipodiopsida, Polytrichopsida, Takakiopsida, Tetraphidopsida</td></tr>
                    <tr><td>c</td><td>h</td><td>non-vascular plants</td><td>Haplomitriopsida</td></tr>
                    <tr><td>c</td><td>j</td><td>non-vascular plants</td><td>Jungermanniopsida</td></tr>
                    <tr><td>c</td><td>m</td><td>non-vascular plants</td><td>Marchantiopsida</td></tr>
                    <tr><td>c</td><td>n</td><td>non-vascular plants</td><td>Anthocerotopsida, Leiosporocerotopsida</td></tr>
                    <tr><td>c</td><td>s</td><td>non-vascular plants</td><td>Sphagnopsida</td></tr>
                    <tr><td>d</td><td>a</td><td>dicotyledons</td><td>Asterales, Berberidopsidales, Boraginales, Dipsacales, Escalloniales, Gentianales, Icacinales, Lamiales, Metteniusales, Paracryphiales, Solanales, Vahliales</td></tr>
                    <tr><td>d</td><td>c</td><td>dicotyledons</td><td>Caryophyllales</td></tr>
                    <tr><td>d</td><td>d</td><td>dicotyledons</td><td>Brassicales, Cucurbitales, Ericales, Malpighiales, Malvales</td></tr>
                    <tr><td>d</td><td>h</td><td>dicotyledons</td><td>Fagales</td></tr>
                    <tr><td>d</td><td>m</td><td>dicotyledons</td><td>Austrobaileyales, Canellales, Ceratophyllales, Chloranthales, Laurales, Magnoliales, Nymphaeales, Piperales, Ranunculales</td></tr>
                    <tr><td>d</td><td>r</td><td>dicotyledons</td><td>Apiales, Aquifoliales, Bruniales, Buxales, Celastrales, Cornales, Crossosomatales, Fabales, Garryales, Geraniales, Gunnerales, Huerteales, Myrtales, Oxalidales, Picramniales, Proteales, Rosales, Santalales, Sapindales, Saxifragales, Vitales, Zygophyllales</td></tr>
                    <tr><td>d</td><td>x</td><td>dicotyledons</td><td>Amborellales, Dilleniales, Trochodendrales</td></tr>
                    <tr><td>e</td><td>a</td><td>echinoderms</td><td>Asteroidea</td></tr>
                    <tr><td>e</td><td>c</td><td>echinoderms</td><td>Crinoidea</td></tr>
                    <tr><td>e</td><td>e</td><td>echinoderms</td><td>Echinoidea</td></tr>
                    <tr><td>e</td><td>h</td><td>echinoderms</td><td>Holothuroidea</td></tr>
                    <tr><td>e</td><td>o</td><td>echinoderms</td><td>Ophiuroidea</td></tr>
                    <tr><td>f</td><td></td><td>fishes</td><td>Actinopterygii</td></tr>
                    <tr><td>g</td><td>a</td><td>fungi</td><td>unspecified_class_Ascomycota, Xylonomycetes</td></tr>
                    <tr><td>g</td><td>b</td><td>fungi</td><td>Bartheletiomycetes, Dacrymycetes, Entorrhizomycetes, Geminibasidiomycetes, Spiculogloeomycetes, unspecified_class_Basidiomycota, Wallemiomycetes, Wallemiomycetes</td></tr>
                    <tr><td>g</td><td>c</td><td>fungi</td><td>Blastocladiomycetes, Chytridiomycetes, Monoblepharidomycetes, Neocallimastigomycetes, Olpidiomycota</td></tr>
                    <tr><td>g</td><td>d</td><td>fungi</td><td>Arthoniomycetes, Dothideomycetes</td></tr>
                    <tr><td>g</td><td>f</td><td>fungi</td><td>Agaricomycetes, Dacrymycetes, Tremellomycetes</td></tr>
                    <tr><td>g</td><td>g</td><td>fungi</td><td>Glomeromycetes, Mucoromycota</td></tr>
                    <tr><td>g</td><td>k</td><td>fungi</td><td>Agaricostilbomycetes, Atractiellomycetes, Classiculomycetes, Cryptomycocolacomycetes, Cystobasidiomycetes, Microbotryomycetes, Mixiomycetes, Pucciniomycetes, Tritirachiomycetes</td></tr>
                    <tr><td>g</td><td>l</td><td>fungi</td><td>Arthoniomycetes, Candelariomycetes, Lecanoromycetes, Lichinomycetes</td></tr>
                    <tr><td>g</td><td>m</td><td>fungi</td><td>Microsporea</td></tr>
                    <tr><td>g</td><td>o</td><td>fungi</td><td>Hyphochytrea, Peronosporea, unspecified_class_Oomycota</td></tr>
                    <tr><td>g</td><td>p</td><td>fungi</td><td>Collemopsidiomycetes, Coniocybomycetes, Eurotiomycetes, Geoglossomycetes, Orbiliomycetes, Pezizomycetes, Xylobotryomycetes</td></tr>
                    <tr><td>g</td><td>r</td><td>fungi</td><td>Sordariomycetes</td></tr>
                    <tr><td>g</td><td>s</td><td>fungi</td><td>Saccharomycetes</td></tr>
                    <tr><td>g</td><td>t</td><td>fungi</td><td>Archaeorhizomycetes, Neolectomycetes, Pneumocystidomycetes, Schizosaccharomycetes, Taphrinomycetes</td></tr>
                    <tr><td>g</td><td>u</td><td>fungi</td><td>Exobasidiomycetes, Malasseziomycetes, Moniliellomycetes, Ustilaginomycetes</td></tr>
                    <tr><td>g</td><td>x</td><td>fungi</td><td>Aphelidea, Cryptomycota, unspecified_phylum_Fungi</td></tr>
                    <tr><td>g</td><td>y</td><td>fungi</td><td>Laboulbeniomycetes, Leotiomycetes</td></tr>
                    <tr><td>g</td><td>z</td><td>fungi</td><td>unspecified_class_Zygomycota, Zoopagomycota</td></tr>
                    <tr><td>h</td><td>c</td><td>platyhelminths</td><td>Catenulida</td></tr>
                    <tr><td>h</td><td>e</td><td>platyhelminths</td><td>Cestoda</td></tr>
                    <tr><td>h</td><td>m</td><td>platyhelminths</td><td>Monogenea</td></tr>
                    <tr><td>h</td><td>r</td><td>platyhelminths</td><td>Rhabditophora</td></tr>
                    <tr><td>h</td><td>t</td><td>platyhelminths</td><td>Trematoda</td></tr>
                    <tr><td>i</td><td>a</td><td>insects</td><td>Archaeognatha</td></tr>
                    <tr><td>i</td><td>b</td><td>insects</td><td>Blattodea, Grylloblattodea, Mantophasmatodea</td></tr>
                    <tr><td>i</td><td>c</td><td>insects</td><td>Coleoptera</td></tr>
                    <tr><td>i</td><td>d</td><td>insects</td><td>Diptera</td></tr>
                    <tr><td>i</td><td>e</td><td>insects</td><td>Ephemeroptera</td></tr>
                    <tr><td>i</td><td>f</td><td>insects</td><td>Phasmida</td></tr>
                    <tr><td>i</td><td>g</td><td>insects</td><td>Dermaptera</td></tr>
                    <tr><td>i</td><td>h</td><td>insects</td><td>Hemiptera</td></tr>
                    <tr><td>i</td><td>i</td><td>insects</td><td>Trichoptera</td></tr>
                    <tr><td>i</td><td>j</td><td>insects</td><td>Mecoptera</td></tr>
                    <tr><td>i</td><td>k</td><td>insects</td><td>Megaloptera</td></tr>
                    <tr><td>i</td><td>l</td><td>insects</td><td>Lepidoptera</td></tr>
                    <tr><td>i</td><td>m</td><td>insects</td><td>Mantodea</td></tr>
                    <tr><td>i</td><td>n</td><td>insects</td><td>Neuroptera</td></tr>
                    <tr><td>i</td><td>o</td><td>insects</td><td>Odonata</td></tr>
                    <tr><td>i</td><td>p</td><td>insects</td><td>Embioptera, Plecoptera, Zoraptera</td></tr>
                    <tr><td>i</td><td>q</td><td>insects</td><td>Orthoptera</td></tr>
                    <tr><td>i</td><td>r</td><td>insects</td><td>Raphidioptera</td></tr>
                    <tr><td>i</td><td>s</td><td>insects</td><td>Siphonaptera</td></tr>
                    <tr><td>i</td><td>t</td><td>insects</td><td>Thysanoptera</td></tr>
                    <tr><td>i</td><td>u</td><td>insects</td><td>Psocodea</td></tr>
                    <tr><td>i</td><td>v</td><td>insects</td><td>Strepsiptera</td></tr>
                    <tr><td>i</td><td>y</td><td>insects</td><td>Hymenoptera</td></tr>
                    <tr><td>i</td><td>z</td><td>insects</td><td>Zygentoma</td></tr>
                    <tr><td>j</td><td>a</td><td>jellyfish and other cnidaria</td><td>Anthozoa</td></tr>
                    <tr><td>j</td><td>c</td><td>jellyfish and other cnidaria</td><td>Cubozoa</td></tr>
                    <tr><td>j</td><td>h</td><td>jellyfish and other cnidaria</td><td>Hydrozoa</td></tr>
                    <tr><td>j</td><td>m</td><td>jellyfish and other cnidaria</td><td>Myxozoa</td></tr>
                    <tr><td>j</td><td>n</td><td>jellyfish and other cnidaria</td><td>Nuda</td></tr>
                    <tr><td>j</td><td>p</td><td>jellyfish and other cnidaria</td><td>Polypodiozoa</td></tr>
                    <tr><td>j</td><td>r</td><td>jellyfish and other cnidaria</td><td>Staurozoa</td></tr>
                    <tr><td>j</td><td>s</td><td>jellyfish and other cnidaria</td><td>Scyphozoa</td></tr>
                    <tr><td>j</td><td>t</td><td>jellyfish and other cnidaria</td><td>Tentaculata</td></tr>
                    <tr><td>k</td><td>a</td><td>other chordates</td><td>Ascidiacea</td></tr>
                    <tr><td>k</td><td>c</td><td>other chordates</td><td>Cephalaspidomorphi, Hyperoartia</td></tr>
                    <tr><td>k</td><td>d</td><td>other chordates</td><td>Appendicularia</td></tr>
                    <tr><td>k</td><td>e</td><td>other chordates</td><td>Enteropneusta</td></tr>
                    <tr><td>k</td><td>l</td><td>other chordates</td><td>Leptocardii</td></tr>
                    <tr><td>k</td><td>m</td><td>other chordates</td><td>Myxini</td></tr>
                    <tr><td>k</td><td>p</td><td>other chordates</td><td>Pterobranchia</td></tr>
                    <tr><td>k</td><td>t</td><td>other chordates</td><td>Thaliacea</td></tr>
                    <tr><td>k</td><td>x</td><td>other chordates</td><td>Coelacanthimorpha, Dipnoi, other_chordata</td></tr>
                    <tr><td>l</td><td>a</td><td>monocotyledons</td><td>Alismatales</td></tr>
                    <tr><td>l</td><td>c</td><td>monocotyledons</td><td>Commelinales</td></tr>
                    <tr><td>l</td><td>d</td><td>monocotyledons</td><td>Dioscoreales</td></tr>
                    <tr><td>l</td><td>l</td><td>monocotyledons</td><td>Liliales</td></tr>
                    <tr><td>l</td><td>n</td><td>monocotyledons</td><td>Pandanales</td></tr>
                    <tr><td>l</td><td>o</td><td>monocotyledons</td><td>Acorales</td></tr>
                    <tr><td>l</td><td>p</td><td>monocotyledons</td><td>Poales</td></tr>
                    <tr><td>l</td><td>r</td><td>monocotyledons</td><td>Arecales</td></tr>
                    <tr><td>l</td><td>s</td><td>monocotyledons</td><td>Asparagales</td></tr>
                    <tr><td>l</td><td>t</td><td>monocotyledons</td><td>Petrosaviales</td></tr>
                    <tr><td>l</td><td>z</td><td>monocotyledons</td><td>Zingiberales</td></tr>
                    <tr><td>m</td><td></td><td>mammals</td><td>Mammalia</td></tr>
                    <tr><td>n</td><td>a</td><td>nematodes</td><td>Aphelenchida</td></tr>
                    <tr><td>n</td><td>b</td><td>nematodes</td><td>Benthimermithida</td></tr>
                    <tr><td>n</td><td>c</td><td>nematodes</td><td>Dioctophymatida</td></tr>
                    <tr><td>n</td><td>d</td><td>nematodes</td><td>Desmodorida</td></tr>
                    <tr><td>n</td><td>e</td><td>nematodes</td><td>Enoplida</td></tr>
                    <tr><td>n</td><td>f</td><td>nematodes</td><td>Adenophorea</td></tr>
                    <tr><td>n</td><td>g</td><td>nematodes</td><td>Strongylida</td></tr>
                    <tr><td>n</td><td>h</td><td>nematodes</td><td>Monhysterida</td></tr>
                    <tr><td>n</td><td>i</td><td>nematodes</td><td>Araeolaimida</td></tr>
                    <tr><td>n</td><td>j</td><td>nematodes</td><td>Isolaimida</td></tr>
                    <tr><td>n</td><td>k</td><td>nematodes</td><td>Muspiceida</td></tr>
                    <tr><td>n</td><td>l</td><td>nematodes</td><td>Dorylaimida</td></tr>
                    <tr><td>n</td><td>m</td><td>nematodes</td><td>Mermithida</td></tr>
                    <tr><td>n</td><td>n</td><td>nematodes</td><td>Mononchida</td></tr>
                    <tr><td>n</td><td>o</td><td>nematodes</td><td>Desmoscolecida</td></tr>
                    <tr><td>n</td><td>p</td><td>nematodes</td><td>Diplogasterida</td></tr>
                    <tr><td>n</td><td>q</td><td>nematodes</td><td>Rhaptothyreida</td></tr>
                    <tr><td>n</td><td>r</td><td>nematodes</td><td>Rhabditida</td></tr>
                    <tr><td>n</td><td>s</td><td>nematodes</td><td>Spirurida</td></tr>
                    <tr><td>n</td><td>t</td><td>nematodes</td><td>Trichocephalida</td></tr>
                    <tr><td>n</td><td>u</td><td>nematodes</td><td>unspecified_class_Nematoda</td></tr>
                    <tr><td>n</td><td>v</td><td>nematodes</td><td>Trichinellida</td></tr>
                    <tr><td>n</td><td>w</td><td>nematodes</td><td>Triplonchida</td></tr>
                    <tr><td>n</td><td>x</td><td>nematodes</td><td>Chromadorea</td></tr>
                    <tr><td>n</td><td>y</td><td>nematodes</td><td>Tylenchida</td></tr>
                    <tr><td>n</td><td>z</td><td>nematodes</td><td>Plectida</td></tr>
                    <tr><td>o</td><td>c</td><td>sponges</td><td>Calcarea</td></tr>
                    <tr><td>o</td><td>d</td><td>sponges</td><td>Demospongiae</td></tr>
                    <tr><td>o</td><td>h</td><td>sponges</td><td>Hexactinellida</td></tr>
                    <tr><td>o</td><td>o</td><td>sponges</td><td>Homoscleromorpha</td></tr>
                    <tr><td>p</td><td>a</td><td>protists</td><td>Amoebozoa, Breviatea, Dictyostelea, Discosea, Evosea, Tubulinea</td></tr>
                    <tr><td>p</td><td>b</td><td>protists</td><td>Bigyra</td></tr>
                    <tr><td>p</td><td>c</td><td>protists</td><td>Cercozoa, Endomyxa, Imbricatea</td></tr>
                    <tr><td>p</td><td>e</td><td>protists</td><td>Euglenozoa</td></tr>
                    <tr><td>p</td><td>f</td><td>protists</td><td>Foraminifera, Globothalamea</td></tr>
                    <tr><td>p</td><td>h</td><td>protists</td><td>Phoronida</td></tr>
                    <tr><td>p</td><td>i</td><td>protists</td><td>Ciliophora</td></tr>
                    <tr><td>p</td><td>k</td><td>protists</td><td>Choanoflagellata, Choanozoa</td></tr>
                    <tr><td>p</td><td>m</td><td>protists</td><td>Mycetozoa</td></tr>
                    <tr><td>p</td><td>p</td><td>protists</td><td>Percolozoa</td></tr>
                    <tr><td>p</td><td>r</td><td>protists</td><td>Rotifera</td></tr>
                    <tr><td>p</td><td>s</td><td>protists</td><td>Sarcomastigophora</td></tr>
                    <tr><td>p</td><td>u</td><td>protists</td><td>Acantharea, Actinophryidae, Aurearenophyceae, Bigyra, Bolidophyceae, Filasterea, Fornicata, Haptista, Heterolobosea, Hyphochytriomycetes, Ichthyosporea, Katablepharidophyta, Labyrinthulomycetes, Parabasalia, Phaeothamniophyceae, Picozoa, Placididea, Polycystinea, Preaxostyla, Raphidophyceae, Rhodelphea, unspecified_phylum_Protozoa</td></tr>
                    <tr><td>p</td><td>v</td><td>protists</td><td>Chromerida, Colponemidia, Perkinsozoa</td></tr>
                    <tr><td>p</td><td>x</td><td>protists</td><td>Apicomplexa</td></tr>
                    <tr><td>p</td><td>y</td><td>protists</td><td>Myzozoa</td></tr>
                    <tr><td>q</td><td>a</td><td>other arthropods</td><td>Merostomata</td></tr>
                    <tr><td>q</td><td>b</td><td>other arthropods</td><td>Branchiopoda</td></tr>
                    <tr><td>q</td><td>c</td><td>other arthropods</td><td>Chilopoda</td></tr>
                    <tr><td>q</td><td>d</td><td>other arthropods</td><td>Diplopoda</td></tr>
                    <tr><td>q</td><td>e</td><td>other arthropods</td><td>Entognatha</td></tr>
                    <tr><td>q</td><td>f</td><td>other arthropods</td><td>Cephalocarida</td></tr>
                    <tr><td>q</td><td>h</td><td>other arthropods</td><td>Hexanauplia</td></tr>
                    <tr><td>q</td><td>i</td><td>other arthropods</td><td>Ichthyostraca</td></tr>
                    <tr><td>q</td><td>l</td><td>other arthropods</td><td>Collembola</td></tr>
                    <tr><td>q</td><td>m</td><td>other arthropods</td><td>Malacostraca</td></tr>
                    <tr><td>q</td><td>o</td><td>other arthropods</td><td>Ostracoda</td></tr>
                    <tr><td>q</td><td>p</td><td>other arthropods</td><td>Pauropoda</td></tr>
                    <tr><td>q</td><td>q</td><td>other arthropods</td><td>Arachnida</td></tr>
                    <tr><td>q</td><td>r</td><td>other arthropods</td><td>Remipedia</td></tr>
                    <tr><td>q</td><td>s</td><td>other arthropods</td><td>Symphyla</td></tr>
                    <tr><td>q</td><td>t</td><td>other arthropods</td><td>Protura</td></tr>
                    <tr><td>q</td><td>u</td><td>other arthropods</td><td>unspecified_class_Arthropoda</td></tr>
                    <tr><td>q</td><td>x</td><td>other arthropods</td><td>Maxillopoda, Mystacocarida</td></tr>
                    <tr><td>q</td><td>y</td><td>other arthropods</td><td>Pycnogonida</td></tr>
                    <tr><td>r</td><td></td><td>reptiles</td><td>Reptilia</td></tr>
                    <tr><td>s</td><td></td><td>sharks</td><td>Chondrichthyes</td></tr>
                    <tr><td>t</td><td>a</td><td>other animal phyla</td><td>Acanthocephala</td></tr>
                    <tr><td>t</td><td>b</td><td>other animal phyla</td><td>Brachiopoda</td></tr>
                    <tr><td>t</td><td>c</td><td>other animal phyla</td><td>Kinorhyncha, Loricifera, Priapulida</td></tr>
                    <tr><td>t</td><td>d</td><td>other animal phyla</td><td>Dicyemida, Rhombozoa</td></tr>
                    <tr><td>t</td><td>e</td><td>other animal phyla</td><td>Entoprocta</td></tr>
                    <tr><td>t</td><td>f</td><td>other animal phyla</td><td>Nematomorpha</td></tr>
                    <tr><td>t</td><td>g</td><td>other animal phyla</td><td>Gastrotricha</td></tr>
                    <tr><td>t</td><td>h</td><td>other animal phyla</td><td>Chaetognatha</td></tr>
                    <tr><td>t</td><td>m</td><td>other animal phyla</td><td>Gnathostomulida</td></tr>
                    <tr><td>t</td><td>n</td><td>other animal phyla</td><td>Nemertea</td></tr>
                    <tr><td>t</td><td>o</td><td>other animal phyla</td><td>Orthonectida</td></tr>
                    <tr><td>t</td><td>s</td><td>other animal phyla</td><td>Sipuncula</td></tr>
                    <tr><td>t</td><td>t</td><td>other animal phyla</td><td>Tardigrada</td></tr>
                    <tr><td>t</td><td>u</td><td>other animal phyla</td><td>Hemimastigophora, Micrognathozoa, Onychophora, Placozoa, unspecified_phylum_Animalia</td></tr>
                    <tr><td>t</td><td>x</td><td>other animal phyla</td><td>Xenacoelomorpha</td></tr>
                    <tr><td>t</td><td>y</td><td>other animal phyla</td><td>Cycliophora</td></tr>
                    <tr><td>t</td><td>z</td><td>other animal phyla</td><td>Bryozoa</td></tr>
                    <tr><td>u</td><td>c</td><td>algae</td><td>Chlorophyta</td></tr>
                    <tr><td>u</td><td>g</td><td>algae</td><td>Glaucophyta</td></tr>
                    <tr><td>u</td><td>h</td><td>algae</td><td>Haptophyta</td></tr>
                    <tr><td>u</td><td>k</td><td>algae</td><td>Charophyta</td></tr>
                    <tr><td>u</td><td>o</td><td>algae</td><td>Bacillariophyceae, Bolidophyceae, Chrysomerophyceae, Chrysophyceae, Chrysophyceae, Dictyochophyceae, Eustigmatophyceae, Ochrophyta, Pelagophyceae, Phaeophyceae, Phaeophyceae, Pinguiophyceae, Synurophyceae, Xanthophyceae</td></tr>
                    <tr><td>u</td><td>r</td><td>algae</td><td>Rhodophyta</td></tr>
                    <tr><td>u</td><td>s</td><td>algae</td><td>Synchromophyceae</td></tr>
                    <tr><td>u</td><td>y</td><td>algae</td><td>Cryptophyta</td></tr>
                    <tr><td>v</td><td>e</td><td>other vascular plants</td><td>Equisetopsida</td></tr>
                    <tr><td>v</td><td>g</td><td>other vascular plants</td><td>Ginkgoopsida</td></tr>
                    <tr><td>v</td><td>l</td><td>other vascular plants</td><td>Lycopodiopsida</td></tr>
                    <tr><td>v</td><td>o</td><td>other vascular plants</td><td>Polypodiopsida</td></tr>
                    <tr><td>v</td><td>p</td><td>other vascular plants</td><td>Cycadopsida, Gnetopsida, Pinopsida</td></tr>
                    <tr><td>v</td><td>s</td><td>other vascular plants</td><td>Psilotopsida</td></tr>
                    <tr><td>w</td><td>a</td><td>annelids</td><td>Amphinomida</td></tr>
                    <tr><td>w</td><td>b</td><td>annelids</td><td>Branchiobdellida</td></tr>
                    <tr><td>w</td><td>c</td><td>annelids</td><td>Acanthobdellida, Crassiclitellata, Hirudinida, Moniligastrida, other_clitellata</td></tr>
                    <tr><td>w</td><td>d</td><td>annelids</td><td>Spionida</td></tr>
                    <tr><td>w</td><td>e</td><td>annelids</td><td>Echiuroidea</td></tr>
                    <tr><td>w</td><td>f</td><td>annelids</td><td>Flabelligerida</td></tr>
                    <tr><td>w</td><td>g</td><td>annelids</td><td>Golfingiida</td></tr>
                    <tr><td>w</td><td>h</td><td>annelids</td><td>Haplotaxida</td></tr>
                    <tr><td>w</td><td>j</td><td>annelids</td><td>Eunicida</td></tr>
                    <tr><td>w</td><td>k</td><td>annelids</td><td>Arhynchobdellida</td></tr>
                    <tr><td>w</td><td>l</td><td>annelids</td><td>Lumbriculida</td></tr>
                    <tr><td>w</td><td>n</td><td>annelids</td><td>Enchytraeida</td></tr>
                    <tr><td>w</td><td>o</td><td>annelids</td><td>Opisthopora</td></tr>
                    <tr><td>w</td><td>p</td><td>annelids</td><td>Phyllodocida</td></tr>
                    <tr><td>w</td><td>r</td><td>annelids</td><td>Rhynchobdellida</td></tr>
                    <tr><td>w</td><td>s</td><td>annelids</td><td>Sabellida</td></tr>
                    <tr><td>w</td><td>t</td><td>annelids</td><td>Aspidosiphonidormes, Terebellida</td></tr>
                    <tr><td>w</td><td>u</td><td>annelids</td><td>Phascolosomatiformes, Potamodrilidae, unspecified_order_Polychaeta, Xenopneusta</td></tr>
                    <tr><td>w</td><td>x</td><td>annelids</td><td>Capitellida, other_annelida, Scolecida</td></tr>
                    <tr><td>x</td><td>a</td><td>molluscs</td><td>Caudofoveata</td></tr>
                    <tr><td>x</td><td>b</td><td>molluscs</td><td>Bivalvia</td></tr>
                    <tr><td>x</td><td>c</td><td>molluscs</td><td>Cephalopoda</td></tr>
                    <tr><td>x</td><td>g</td><td>molluscs</td><td>Gastropoda</td></tr>
                    <tr><td>x</td><td>m</td><td>molluscs</td><td>Monoplacophora</td></tr>
                    <tr><td>x</td><td>o</td><td>molluscs</td><td>Solenogastres</td></tr>
                    <tr><td>x</td><td>p</td><td>molluscs</td><td>Polyplacophora</td></tr>
                    <tr><td>x</td><td>s</td><td>molluscs</td><td>Scaphopoda</td></tr>
                    <tr><td>y</td><td>a</td><td>bacteria</td><td>Actinobacteria</td></tr>
                    <tr><td>y</td><td>c</td><td>bacteria</td><td>Cyanobacteria</td></tr>
                    <tr><td>y</td><td>p</td><td>bacteria</td><td>Proteobacteria</td></tr>
                    <tr><td>z</td><td></td><td>archaea</td><td>Archaea</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;