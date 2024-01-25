<!-- Footer
   ============================================= -->

    <footer id="footer" class="dark border-0">

    <div class="text-center" style="background-color: rgba(0, 0, 0, 0.2)">

        <div class="row mx-auto" style="padding-top: 30px">

            <div class="col-lg-4">
            </div>

            <div class="col-lg-4">

                <div class="widget ">
                    <h3>Dive into next-gen journalism with Mindbugs Discovery! 📰 Join now for exclusive early access. 🌐</h3>

                    <form action="<?=base_url()?>/home/joinWaitList" method="post" class="mb-0">
                        <input type="email" id="email" name="email" class="form-control form-control-lg not-dark required email" placeholder="Your Email Address">
                        <button class="button button-border button-circle button-light mt-4" type="submit">Join Now</button>
                    </form>
                </div>

            </div>

            <div class="col-lg-4">
            </div>

        </div>
    </div>

    <div id="copyrights">
        <div class="container">
            <div class="row">
                <div class="col-md-4 col-sm-4 center" style="justify-content: center; display: flex; flex-direction: column;">
                    <strong>Phone:<a href="tel:+40769693891"> +40 769 69 3891</a></strong><br>
                    <strong>Email:<a href = "mailto: contact@techwave.ro"> contact@techwave.ro</a></strong>
                </div>
                <div class="col-md-4 col-sm-4 center" style="display: flex; flex-direction: column;">
                    <div class="d-flex justify-content-center mt-4">
                        <a href="https://www.linkedin.com/company/mindbugs-official/" style="color: rgba(255, 255, 255, 0.4); margin-top: 5px">Follow us!</a>
                        <a href="https://www.linkedin.com/company/mindbugs-official/" class="social-icon si-small bg-transparent h-bg-linkedin" title="Linkedin">
                            <i class="fa-brands fa-linkedin"></i>
                            <i class="fa-brands fa-linkedin"></i>
                        </a>
                    </div>
                </div>
                <div class="col-md-4 col-sm-4 center">
                    <img style="width:120px; margin-right:50px; margin-left: -40px" src="<?=base_url()?>/public/layout/logo/eu_flag.png">
                    <img style="width:120px;" src="<?=base_url()?>/public/layout/logo/mie_white.png">
                    <img style="width:120px; margin-right: 50px" src="<?=base_url()?>/public/layout/logo/ai4media_logo.png">
                    <img style="width:160px" src="<?=base_url()?>/public/layout/logo/ngiSearch.png">
                </div>
            </div>
            <div class="row justify-content-center" style="font-size:12px">

                <div class="col-sm-6 center">
                    The MindBugs Discovery has indirectly received funding from the European Union’s Horizon 2020 research and innovation action programme, via the AI4Media Open Call #2 issued and executed under the AI4Media project (Grant Agreement no. 951911).

                </div>
                <div class="col-sm-6 center">
                    Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or European Commission. Neither the European Union nor the granting authority can be held responsible for them. Funded within the framework of the NGI Search project under grant agreement No 101069364.
                </div>
            </div>

        </div>
    </div>

</footer><!-- #footer end -->

</div><!-- #wrapper end -->

<!-- Go To Top
============================================= -->
<div id="gotoTop" class="uil uil-angle-up"></div>

<!-- JavaScripts
============================================= -->
<script src="<?=base_url()?>/public/layout/canva/js/plugins.min.js"></script>
<script src="<?=base_url()?>/public/layout/canva/js/functions.bundle.js"></script>

<?php if(session()->getFlashdata('error')):?>
    <script>
        Swal.fire({
            icon: 'error',
            title: '<?=session()->getFlashdata('error')?>',
            confirmButtonText: 'Ok'
        })
    </script>
<?php endif;?>
<?php if(session()->getFlashdata('success')):?>
    <script>
        Swal.fire({
            icon: 'success',
            title: '<?=session()->getFlashdata('success')?>',
            confirmButtonText: 'Ok'
        })
    </script>
<?php endif;?>

</body>
</html>