<!-- Page Title
============================================= -->
<section class="page-title bg-transparent">
    <div class="container">
        <div class="page-title-row">

            <div class="page-title-content">
                <h1>Blog</h1>
                <span>Our Latest News</span>
            </div>

            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="<?=base_url()?>">Home</a></li>
                    <li class="breadcrumb-item active" aria-current="page">Blog</li>
                </ol>
            </nav>

        </div>
    </div>
</section><!-- .page-title end -->

<!-- Content
============================================= -->
<section id="content">
    <div class="content-wrap">
        <div class="container">
            <div id="posts" class="row gutter-40">

                <div class="entry col-12">
                    <div class="grid-inner row g-0">
                        <div class="col-md-4">
                            <div class="entry-image">
                                <a href="<?=base_url()?>/public/layout/blog/arhitecture.png" data-lightbox="image"><img src="<?=base_url()?>/public/layout/blog/arhitecture.png" alt="Mindbugs Discovery"></a>
                            </div>
                        </div>
                        <div class="col-md-8 ps-md-4">
                            <div class="entry-title title-sm">
                                <h2><a href="<?=base_url()?>/blog/mindbugs-discovery-technical-implementation">Technical implementation of MindBugs Discovery</a></h2>
                            </div>
                            <div class="entry-meta">
                                <ul>
                                    <li><i class="uil uil-schedule"></i> 10h Nov 2023</li>
                                    <li><a href="#"><i class="uil uil-user"></i> Ioana Cheres</a></li>
                                    <li><i class="uil uil-folder-open"></i> <a>General</a>, <a>Media</a></li>
                                </ul>
                            </div>
                            <div class="entry-content">
                                <p>MindBugs Discovery is a platform designed to combat misinformation by integrating
                                    state-of-the-art machine learning techniques with knowledge graph technology.
                                </p>
                                <p>The platform aggregates data from verified fact-checking organizations across
                                    Europe, providing a centralized repository of reliable information.
                                </p>
                                <a href="<?=base_url()?>/blog/deep-dive-veridica-database" class="more-link">Read More</a>
                            </div>
                        </div>
                    </div>
                </div>


                <div class="entry col-12">
                    <div class="grid-inner row g-0">
                        <div class="col-md-4">
                            <div class="entry-image">
                                <a href="<?=base_url()?>/public/layout/blog/graph_small.png" data-lightbox="image"><img src="<?=base_url()?>/public/layout/blog/graph_small.png" alt="Mindbugs Discovery"></a>
                            </div>
                        </div>
                        <div class="col-md-8 ps-md-4">
                            <div class="entry-title title-sm">
                                <h2><a href="<?=base_url()?>/blog/deep-dive-veridica-database">Deep Dive into the Veridica Fact Check Database</a></h2>
                            </div>
                            <div class="entry-meta">
                                <ul>
                                    <li><i class="uil uil-schedule"></i> 15th Oct 2023</li>
                                    <li><a href="#"><i class="uil uil-user"></i> Ioana Cheres</a></li>
                                    <li><i class="uil uil-folder-open"></i> <a>General</a>, <a>Media</a></li>
                                </ul>
                            </div>
                            <div class="entry-content">
                                <p>Our team recently analyzed the Veridica database, a complex set of fact-check articles. With a significant number of 617 entries extracted, some interesting patterns emerged regarding the most frequent terms and entities.
                                </p>
                                <p>To structure and analyze the data, all statements were organized within a Neo4J graph. Each statement was linked to the entities involved, the channels through which information propagated, and relevant political figures.</p>
                                <a href="<?=base_url()?>/blog/deep-dive-veridica-database" class="more-link">Read More</a>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="entry col-12">
                    <div class="grid-inner row g-0">
                        <div class="col-md-4">
                            <div class="entry-image">
                                <a href="<?=base_url()?>/public/layout/blog/kg.png" data-lightbox="image"><img src="<?=base_url()?>/public/layout/blog/kg.png" alt="Mindbugs KG"></a>
                            </div>
                        </div>
                        <div class="col-md-8 ps-md-4">
                            <div class="entry-title title-sm">
                                <h2><a href="<?=base_url()?>/blog/mindbugs-journalistic-tool">Mindbugs Journalistic Tool</a></h2>
                            </div>
                            <div class="entry-meta">
                                <ul>
                                    <li><i class="uil uil-schedule"></i> 18th May 2023</li>
                                    <li><a href="#"><i class="uil uil-user"></i> Ioana Cheres</a></li>
                                    <li><i class="uil uil-folder-open"></i> <a>General</a>, <a>Media</a></li>
                                </ul>
                            </div>
                            <div class="entry-content">
                                <p>The nexus between AI4Media and Media Blend provides an unparalleled platform for MindBugs. In the rapidly evolving ecosystem of technology and media, the importance of creating powerful tools based on artificial intelligence is a crucial aspect in fighting misinformation. Find out more about the MindBugs discovery journalistic tool.</p>
                                <a href="<?=base_url()?>/blog/mindbugs-journalistic-tool" class="more-link">Read More</a>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</section><!-- #content end -->
