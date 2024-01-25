
<section class="page-title bg-transparent">
    <div class="container">
        <div class="page-title-row">

            <div class="page-title-content">
                <h1>Deep Dive into the Veridica Fact Check Database</h1>
            </div>
            <br>
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="<?=base_url()?>">Home</a></li>
                    <li class="breadcrumb-item"><a href="<?=base_url()?>/blog">Blog</a></li>
                </ol>
            </nav>

        </div>
    </div>
</section>

<!-- Content
============================================= -->
<section id="content">
    <div class="content-wrap">
        <div class="container">

            <div class="single-post mb-0">

                <div class="entry">

                    <div class="entry-title">
                        <h2></h2>
                    </div>

                    <div class="entry-meta">
                        <ul>
                            <li><i class="uil uil-schedule"></i> 15th Oct 2023</li>
                            <li><a href="#"><i class="uil uil-user"></i> Ioana Cheres</a></li>
                            <li><i class="uil uil-folder-open"></i>General, Media</li>
                        </ul>
                    </div>
                    <div class="entry-content mt-0">
                        <p>
                            Our team recently analyzed the Veridica database, a complex set of fact-check articles. With a significant number of 617 entries extracted, some interesting patterns emerged regarding the most frequent terms and entities.
                        </p>
                    </div>

                    <div class="entry-content mt-0">
                        <p>
                            To structure and analyze the data, all statements were organized within a Neo4J graph. Each statement was linked to the entities involved, the channels through which information propagated, and relevant political figures.
                        </p>
                    </div>

                    <div class="entry-content mt-0">
                        <p>
                            Analyzing word frequency across various texts provides insights into the central themes and subjects of discussion. In our analysis, we have identified the three most highly connected entities: "Ukraine" with 422 connections, "Russia" with 366 connections, and "Romania" with 175 connections. This finding suggests a potential correlation between disinformation statements and the prevailing national sentiment among the populace.
                        </p>
                    </div>
                    <div class="entry-content mt-0">
                        <div class="entry-image aligncenter" style="max-width: 500px!important;">
                            <a style="text-align: center; font-size: 14px;font-style: italic;"><img src="<?=base_url()?>/public/layout/blog/graph_small.png" alt="Graph subset: one statement analysis">Graph subset: one statement analysis</a>
                        </div>
                    </div>
                    <div class="entry-content mt-0">
                        <p>
                            Delving into the assessment of frequently used propagation channels, "ukraina.ru" emerges as the source of 68 disinformation statements within the dataset, closely followed by "sputnik.md" with 56, and "ria.ru" with 43.
                        </p>
                        <p>
                            Turning our attention to the most frequently mentioned individuals, we observe a notable decrease in frequency. The "Volodymyr Zelenskyy" node is connected to 30 disinformation statements, "Vladimir Putin" to 20, and "Igor Dondon" to 11.
                        </p>
                        <p>
                            It's important to note that rather than providing a definitive depiction of misinformation, this article offers a concise glimpse into the narratives explored by the Veridica organization. The emphasis on certain countries, individuals, or narratives within the dataset may influence the higher numbers associated with them.
                        </p>
                        <p>
                            For those seeking a more comprehensive understanding of propaganda narratives, their structure, interconnections, and origins, we encourage you to visit our website at www.discovery.mindbugs.ro. Our project is still in its early stages, and we aspire to contribute to the protection of democracy by enhancing the efficiency of fact-checking organizations and promoting transparency in information dissemination.
                        </p>
                    </div>
                    <div class="row">
                        <div class="col-md-2 col-sm-12" style="display: grid; align-items: center; justify-content: center">
                            <img src="<?= base_url()?>/public/layout/logo/eu_flag.png" alt="Eu Flag"/>
                        </div>
                        <div class="col-md-2 col-sm-12" style="display: grid; align-items: center; justify-content: center">
                            <img src="<?= base_url()?>/public/layout/logo/AI4Media.jpg" style="height: 80px" alt="Ai4Media"/>
                        </div>
                        <div class="col-md-8 col-sm-12" style="display: grid; align-items: center"><p>
                                The MindBugs Discovery has indirectly received
                                funding from the European Union’s Horizon 2020 research and innovation action
                                programme, via the AI4Media Open Call #2 issued and executed under the AI4Media
                                project (Grant Agreement no. 951911).</p>
                                <p>
                                Any promotion made by the beneficiary about the project, in whatever form and by whatever medium reflects only the author’s views and that the EC or the AI4Media
                                project is not responsible for any use that may be made of the information contained therein.</p>
                        </div>
                    </div>

                    <div class="entry-image mb-5">
                        <a style="text-align: center; font-size: 14px;font-style: italic;"><img src="<?=base_url()?>/public/layout/blog/graph.png" alt="Subgraph sample">Subgraph sample</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section><!-- #content end -->