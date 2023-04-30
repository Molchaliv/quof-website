# Quof Website

Quof - Open source software for editing text files

In order for more people to learn about this program, a website was developed. The site uses the `flask` web framework and related extensions. In addition, the `markdown` library was used to create documentation by site administrators.

To download, you must log in or use an `API` key. `API` key can be obtained only after registration. The site also has a documentation page. So far, there is nothing interesting on it, but in the future the documentation will expand.

The download will download the latest version of the software, but you can also download any other version:

`/download/<version>`

![Main page screenshot](https://raw.githubusercontent.com/Molchaliv/quof-website/main/screenshots/index-page-screenshot.png)

## Some results

The site will be expanded in the future. Password recovery, profile editing, email verification and more will be added.

## Requirements

    Flask==2.2.3
    Flask-Login==0.6.2
    Flask-SQLAlchemy==3.0.3
    Markdown==3.4.3
