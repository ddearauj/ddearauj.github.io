from string import Template
import yaml
from pathlib import Path

main_html_template = Template(
    """
    <!DOCTYPE html>
    <html class="no-js" lang="en">

    <head>
        $head
    </head>

    <body id="top">

        $preloader

        $header

        $content

        $footer

        $scripts

    </body>

</html>
    """
)


def generate_html(main_template: Template, kwargs: dict):
    """"""

    return main_template.substitute(
        head=generate_head(kwargs["page_title"]),
        preloader=generate_preloader(),
        header=generate_header(),
        content=kwargs["html_content_func"](**kwargs),
        footer=generate_footer(),
        scripts=generate_scripts(),
    )


def generate_head(page_title):
    return f"""
    <!--- basic page needs
    ================================================== -->
    <meta charset="utf-8">
    <title>{page_title} - deve ser aqui</title>
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- mobile specific metas
    ================================================== -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- CSS
    ================================================== -->
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="stylesheet" href="/css/vendor.css">

    <!-- script
    ================================================== -->
    <script src="/js/modernizr.js"></script>

    <!-- favicons
    ================================================== -->
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <link rel="manifest" href="site.webmanifest">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">

    """


def generate_preloader():
    return """
    <div id="preloader">
        <div id="loader"></div>
    </div>
    """


def generate_header():
    return """
    <header class="s-header">
        <div class="row s-header__content">
            <div class="s-header__logo">
                <a class="logo" href="index.html">
                    <img src="/images/heart-svgrepo-com.svg" alt="Homepage">
                </a>
            </div>

            <nav class="s-header__nav-wrap">

                <h2 class="s-header__nav-heading h6">Site Navigation</h2>

                <ul class="s-header__nav">
                    <li><a href="index.html" title="">Home</a></li>
                    <li><a href="categorias.html" title="">Categorias</a></li>
                    <li><a href="about.html" title="">Sobre</a></li>
                </ul> <!-- end header__nav -->

                <a href="#0" title="Close Menu" class="s-header__overlay-close close-mobile-menu">Close</a>

            </nav> <!-- end header__nav-wrap -->

            <a class="s-header__toggle-menu" href="#0" title="Menu"><span>Menu</span></a>


        </div> <!-- end s-header__content -->

    </header> <!-- end header -->
    
    """


def get_list_of_categorias(pages_dict):
    category_list = []
    for _, page_dict in pages_dict["posts"].items():
        cat = page_dict["category"]
        if cat not in category_list:
            category_list.append(cat)

    return category_list


def generate_page_categorias(**kwargs):
    main_img_path = kwargs.get("main_img_path")
    title = kwargs.get("post_title")
    category_list = kwargs.get("category_list")

    category_code_string = """ """
    for category in category_list:
        cat_html = get_cat_html(category)
        category_code_string += (
            f"""<li><a href="/categorias/{cat_html}.html" title="">{category}</a></li> """
        )
        print(category_code_string)

    return f"""
    <section class="s-content">
        <div class="row">
            <div class="column large-12">

                <section>

                    <div class="s-content__media">
                        <img src="{main_img_path}" sizes="(max-width: 2100px) 100vw, 2100px" alt="">
                    </div> <!-- end s-content__media -->

                    <div class="s-content__primary">

                        <h1 class="s-content__title">{title}</h1>

                        {category_code_string}
                        <hr>

                    </div> <!-- end s-content__primary -->

                </section>

            </div> <!-- end column -->
        </div> <!-- end row -->
    </section> <!-- end s-content -->
    """


def generate_about_content(**kwargs):
    main_img_path = kwargs.get("main_img_path")
    title = kwargs.get("post_title")
    text = kwargs.get("post_text")

    return f"""
    <section class="s-content">
        <div class="row">
            <div class="column large-12">

                <section>

                    <div class="s-content__media">
                        <img src="{main_img_path}" sizes="(max-width: 2100px) 100vw, 2100px" alt="">
                    </div> <!-- end s-content__media -->

                    <div class="s-content__primary">

                        <h1 class="s-content__title">{title}</h1>

                        {text}

                        <hr>
                    </div> <!-- end s-content__primary -->

                </section>

            </div> <!-- end column -->
        </div> <!-- end row -->
    </section> <!-- end s-content -->
    """


def get_cat_html(category: str) -> str:

    if category == "I <3 SP":
        cat_html = "I_LUV_SP"
    elif category == "#GrifosDigitais":
        cat_html = "grifos_digitais"
    else:
        cat_html = category.replace(" ", "_")

    return cat_html


def generate_post_content(**kwargs):
    main_img_path = kwargs.get("main_img_path")
    title = kwargs.get("post_title")
    text = kwargs.get("post_text")
    date = kwargs.get("date")
    category = kwargs.get("category")
    path = kwargs.get("path")

    cat_html = get_cat_html(category)

    return f"""
        <section class="s-content s-content--single">
        <div class="row">
            <div class="column large-12">

                <article class="s-post entry format-standard">

                    <div class="s-content__media">
                        <div class="s-content__post-thumb">
                            <img src="{main_img_path}" sizes="(max-width: 2100px) 100vw, 2100px" alt="">
                        </div>
                    </div> <!-- end s-content__media -->

                    <div class="s-content__primary">

                        <h2 class="s-content__title s-content__title--post"><a href="posts/{path}">{title}</a></h2>

                        <ul class="s-content__post-meta">
                            <li class="date">{date}</li>
                            <li class="cat"><a href="/categorias/{cat_html}.html">{category}</a></li>
                        </ul>

                        {text}

                    </div> <!-- end s-content__primary -->
                </article>

            </div> <!-- end column -->
        </div> <!-- end row -->
    </section> <!-- end s-content -->
    """


def generate_footer():
    return """
    <!-- footer
    ================================================== -->
    <footer class="s-footer">

        <div class="s-footer__bottom">
            <div class="row">
                <div class="column">
                    <div class="ss-copyright">
                        <span>Design by <a href="https://www.styleshout.com/">StyleShout</a></span>
                    </div> <!-- end ss-copyright -->
                </div>
            </div>

            <div class="ss-go-top">
                <a class="smoothscroll" title="Back to Top" href="#top">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M6 4h12v2H6zm5 10v6h2v-6h5l-6-6-6 6z" />
                    </svg>
                </a>
            </div> <!-- end ss-go-top -->
        </div> <!-- end s-footer__bottom -->

    </footer> <!-- end s-footer -->
    """


def generate_footer_feed(current_page, max_page):
    return_html = """ """
    return_html += """
            <div class="column large-12">
                <nav class="pgn">
                    <ul>
                        <li>
                            <a class="pgn__prev" href="#0">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12.707 17.293L8.414 13H18v-2H8.414l4.293-4.293-1.414-1.414L4.586 12l6.707 6.707z"></path></svg>
                            </a>
                        </li>
    """

    for i in range(0, max_page):

        if current_page == i:
            class_str = " current"
        else:
            class_str = ""

        if i == 0:
            return_html += f"""
                <li><a class="pgn__num{class_str}" href="index.html">{i+1}</a></li>
            """

        else:
            return_html += f"""
                <li><a class="pgn__num{class_str}" href="page_{i+1}.html">{i+1}</a></li>
            """



    return_html += """
                        <li>
                            <a class="pgn__next" href="#0">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M11.293 17.293l1.414 1.414L19.414 12l-6.707-6.707-1.414 1.414L15.586 11H6v2h9.586z"></path></svg>
                            </a>
                        </li>
                    </ul>
                </nav> <!-- end pgn -->
            </div> <!-- end column -->

    <!-- footer
    ================================================== -->
    <footer class="s-footer">

        <div class="s-footer__bottom">
            <div class="row">
                <div class="column">
                    <div class="ss-copyright">
                        <span>Design by <a href="https://www.styleshout.com/">StyleShout</a></span>
                    </div> <!-- end ss-copyright -->
                </div>
            </div>

            <div class="ss-go-top">
                <a class="smoothscroll" title="Back to Top" href="#top">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M6 4h12v2H6zm5 10v6h2v-6h5l-6-6-6 6z" />
                    </svg>
                </a>
            </div> <!-- end ss-go-top -->
        </div> <!-- end s-footer__bottom -->

    </footer> <!-- end s-footer -->
    """

    return return_html


def generate_scripts():
    return """
    <!-- Java Script
    ================================================== -->
    <script src="/js/jquery-3.2.1.min.js"></script>
    <script src="/js/plugins.js"></script>
    <script src="/js/main.js"></script>
    """


def generate_feed(main_template: Template, pages_dict: dict):
    feed_html = """"""
    post_counter = 1
    page = 0

    

    for _, page_dict in pages_dict["posts"].items():
        # print(page_dict)
        feed_html += generate_post_content(**page_dict)
        print(f"({post_counter}, {[page]})", end=", ")
        if post_counter % 6 == 0:
            print("opaaaa")
            final_html = main_template.substitute(
                head=generate_head("Feed"),
                preloader=generate_preloader(),
                header=generate_header(),
                content=feed_html,
                footer=generate_footer_feed(current_page=page, max_page=len(pages_dict["posts"].keys())//5),
                scripts=generate_scripts(),
            )
            feed_html = """"""

            if page == 0:
                with open("index.html", "w", encoding="utf-8") as f:
                    f.write(final_html)
                    page += 1
            else:
                page += 1
                with open(f"page_{page}.html", "w", encoding="utf-8") as f:
                    f.write(final_html)
        post_counter+=1

    final_html = main_template.substitute(
        head=generate_head("Feed"),
        preloader=generate_preloader(),
        header=generate_header(),
        content=feed_html,
        footer=generate_footer(),
        scripts=generate_scripts(),
    )

    page += 1
    with open(f"page_{page}.html", "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_category_feed(main_template: Template, pages_dict: dict):
    cat_list = get_list_of_categorias(pages_dict)

    for cat in cat_list:
        feed_html = """"""

        for _, page_dict in pages_dict["posts"].items():
            if page_dict["category"] != cat:
                continue
            # print(page_dict)
            feed_html += generate_post_content(**page_dict)

        final_html = main_template.substitute(
            head=generate_head(f"Feed {cat}"),
            preloader=generate_preloader(),
            header=generate_header(),
            content=feed_html,
            footer=generate_footer(),
            scripts=generate_scripts(),
        )


        with open(f"categorias/{get_cat_html(cat)}.html", "w", encoding="utf-8") as f:
            f.write(final_html)


def generate_pages(main_template: Template, pages_dict: dict):
    # generate pages:
    cat_list = get_list_of_categorias(pages_dict)
    # print(cat_list)

    for _, page_dict in pages_dict["pages"].items():
        page_dict["category_list"] = cat_list
        html = generate_html(main_template, page_dict)

        with open(page_dict["path"], "w", encoding="utf-8") as f:
            f.write(html)

    for _, page_dict in pages_dict["posts"].items():
        html = generate_html(main_template, page_dict)

        with open(f"posts/{page_dict['path']}", "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    pages_dict = yaml.safe_load(
        Path("pages/main_pages.yaml").read_text(encoding="utf-8")
    )

    for key in pages_dict["pages"].keys():
        if key == "about":
            pages_dict["pages"][key]["html_content_func"] = generate_about_content
        if key == "categorias":
            pages_dict["pages"][key]["html_content_func"] = generate_page_categorias

    for key in pages_dict["posts"].keys():
        pages_dict["posts"][key]["html_content_func"] = generate_post_content

    generate_pages(main_template=main_html_template, pages_dict=pages_dict)
    generate_feed(main_template=main_html_template, pages_dict=pages_dict)
    generate_category_feed(main_template=main_html_template, pages_dict=pages_dict)
