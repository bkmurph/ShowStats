import dash
from dash import dcc, html

dash.register_page(__name__, name="About the Site")

layout = html.Div(
    [
        dcc.Markdown(
            """
        # Introduction
        __________________
        I attended my first Widespread Panic show in Charleston, SC at the Trondossa Festival in 2019.
        Little did I know that would be the start of a new hobby that would lead me to see a bunch of
        new bands that I would travel to different parts of the country to see.
        As the shows stacked up, as much as I'd like to think I have a good memory (I don't), it's sometimes
        difficult to remember what songs were played where. I always wished there was a tool where I could
        track the specific shows I went to. One day the lightbulb finally went off that I have the
        skilset to make that happen. This is my attempt at doing just that.
        I think it's pretty cool, hopefully some other people will too.

        # How to Use
        __________________
        1. The app will open up as a blank canvas,
        meaning that none of the plots will be populated.
     
        2. For whichever artists you'd like, open their dropdown container,
        and search (or scroll) to select the shows you'd like to include. In the gif below, I'll
        search for Phish 2022-07-29 (Raleigh) and Widespread Panic 2021-07-17 (Wilmington).
        The date and location of the show will be the most useful key words to use.

        ![](https://showstats1.s3.amazonaws.com/2023-05-27+14.55.37.gif)
        
        3. Press submit and view results!
        
        # Useful Tips
        __________________
        
        1. Each of the plots shown on the site are interactive. This is a nice feature,
        but can cause some issues. One common one is to accidentally select a portion of
        the graph that shows no information. This can be fixed with a double-click
        (or double tap on mobile).
        
        2. If you're viewing the table on mobile, you'll likely only be able to see the artist
        and city initially. Make sure to scroll to the right to see more info!
        
        3. I'll continue to update this section as I collect feedback from users. 
        
        # Acknowledgements
        __________________
        - [Dash](https://dash.plotly.com/) and 
        [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/): 
        These two Python packages abstract many of the HTML/CSS skills needed to build a web app.
        I wouldn't have been able to put together the site without these tools.
   
        - [Dash Forum Community](https://community.plotly.com/c/python/25):
        There are some people on this site that dedicate a large portion of their free time to helping
        others troubleshoot their Dash issues. I'm thankful for their help in parts of the project where
        I was extremely stuck.
     
        - [Relisten.net](https://relisten.net/): Shoutout Relisten for not only providing a free way
        to listen to concerts, but also providing most of the data for this site. It's not perfect,
        but it got me most of the way there. 
        
        - [Jake H. from Shell's Vintage](https://shellsvintage.com/): Special thanks to Jake for designing
        the logo for the site. Go check out his webpage for all of your vintage hat needs!
        
        - The bands: For taking all of my money and inspiring me to make this page.
        
        """
        )
    ]
)
