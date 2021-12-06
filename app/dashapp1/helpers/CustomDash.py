import dash
from app.webapp import get_user



class CustomDash(dash.Dash):
    def interpolate_index(self, **kwargs):
        # Inspect the arguments by printing them
        # print(kwargs)
        nav_bar = """
              <ul class="navbar-nav navbar-right">
                <li class="nav-item">
                  <a class="nav-link" href="/account/login">login</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        """

        if get_user() != None:
            nav_bar = """
              <ul class="navbar-nav navbar-right">
                <li class="nav-item">
                  <a class="nav-link" href="/account/logout">logout</a>
                </li>
              </ul>

            </div>
          </div>
        </nav>
        """

        index_string_top = '''
        <!DOCTYPE html>
        <html>
            <head>
                {metas}
                <title>{title}</title>
                {favicon}
                {css}

                <link href="https://cdn.jsdelivr.net/npm/shareon@1/dist/shareon.min.css" rel="stylesheet">
                <script src="https://cdn.jsdelivr.net/npm/shareon@1/dist/shareon.min.js" type="text/javascript"></script>

            </head>
            <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
          <div class="container-fluid">
            <a class="navbar-brand" href="/">Ghost Rhymes</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarColor01">
              <ul class="navbar-nav me-auto">
                <li class="nav-item">
                  <a class="nav-link active" href="/demo/Rapper">Rapper
                    <span class="visually-hidden">(current)</span>
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link active" href="/demo/Cowboy">Cowboy
                    <span class="visually-hidden">(current)</span>
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/stripe">Train Your Own</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">About</a>
                </li>
              </ul>
        '''
        index_string_bot = '''
                {app_entry}
                <footer>
                    {config}
                    {scripts}
                    {renderer}
                </footer>

                <div style="overflow:hidden;width:40%;margin:auto;margin-top:5%;text-align:center">

                    <div class="shareon" style="overflow:hidden;width:600px;margin:auto;text-align:center;margin-top:5%">
                        <a class="twitter"></a>
                        <a class="linkedin"></a>
                        <a class="reddit"></a>
                        <a class="telegram "data-text="Check this out!"></a>
                        <a class="whatsapp" data-text="Check this out!"></a>
                    </div>
                </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"></script>
                </body>
        </html>
        '''
        index_string = index_string_top + nav_bar + index_string_bot


        return index_string.format(
            app_entry=kwargs['app_entry'],
            config=kwargs['config'],
            scripts=kwargs['scripts'],
            renderer=kwargs['renderer'],
        metas=kwargs['metas'],
        title=kwargs['title'],
        favicon=kwargs['favicon'],
        css=kwargs['css'])



