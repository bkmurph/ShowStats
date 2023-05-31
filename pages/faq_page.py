import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

# import show_stats.ShowStats.helper_functions as hf

dash.register_page(__name__, name="FAQs")


layout = html.Div(
    [
        html.H1("Frequently Asked Questions"),
        html.Hr(),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """
                        Hands down, the best place for ShowStats is on a computer. Using a laptop
                        or desktop will offer the most complete experience. Of course,
                        people use their phones for everything, so I've spent a lot of
                        time making sure that the app does work on mobile devices as well.              
                        """
                        )
                    ],
                    title="Where is the best place to use this site?",
                ),
            ],
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """
                        That's the plan. What's currently available is just a jumping off point.
                        Please reach out with additional charts or information you'd like to see
                        at bkmurphy5@gmail.com!                
                        """
                        )
                    ],
                    title="Are you gonna add more views?",
                ),
            ],
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """
                        As much as I'd like to think this app is perfect, there are going to
                        be issues. If you have any feedback, good, bad, or ugly, please reach out.
                        Even better, if you could open an issue on my
                        [github page](https://github.com/bkmurph/ShowStats/issues), that would
                        be the best way for me to track potential improvements.                  
                        """
                        )
                    ],
                    title="How do I leave feedback?",
                ),
            ],
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """
                        Yea. If I get enough requests I'm happy to try to add new artists.
                        However, more niche artists tend to have alot of data quality issues.
                        If I can't fix those issues programatically, then it doesn't make sense for me
                        to include them (too much manual work).
                        Also, some artists don't have a ton of variance
                        in their setlists, which doesn't work well for this site.              
                        """
                        )
                    ],
                    title="Can you add more artists?",
                ),
            ],
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """
                        Most of them. I'm only able to include what is available
                        on relisten.net and setlist.fm. These sites rely on tapers or
                        indivdual setlist entry. While people usually do a good job,
                         there is human error involved in manual data entry. Depending on
                         the show or artist there may be missing song / data / location /
                          / entire show data.     
                        """
                        )
                    ],
                    title="Do you have every show?",
                ),
            ],
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """
                        1. My Github page. I'm sure there is other developers in the jam band
                        community. I'm open to collaborating if anyone is interested in improving the site.
                        It's also the best place for me to track and
                        (hopefully) address issues. Finally, it allows anyone who is
                        learning Dash or is curious how I built the app to download the repo directly.
                        
                        2. Relisten.net link. I sourced most of the data using the API from this site,
                        I think that is deserving of a free ad.
                        
                        3. Buy Me a Coffee link. I built this site because I wanted to track my own shows.
                        By making it available to the public, there are recurring costs to reserve
                        server space and AWS S3 buckets. I don't expect anything,
                        but if anyone is so inclined, tips are greatly appreciated!       
                        """
                        )
                    ],
                    title="What are the icons on the bottom?",
                ),
            ],
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dcc.Markdown(
                            """
                        Lots of things! Here are some...
                        - Looking into alternative data sources for Relisten.net shows with incomplete or
                        innacurate data (looking at you Billy and Goose).
                        
                        - I would not describe the app as "snappy". It bothers me that it takes a few seconds
                        to load and that going back to the ShowStats tab is really slow. I'm exploring solutions
                        to cache the dataset that feeds the site and hopefully increase the "snappiness".
                        
                        - I need to schedule a refresh of the dataset likely on a weekly basis so new shows are
                        continuously added to the site. I don't think this is that hard, I just haven't done it yet.
                        
                        - Refactoring, refactoring, refactoring! Right now the code to run this site
                        works. However, the perfectionist in me wants the code clean, compact, and readable.
                        Right now it is migraine inducing in certain areas.
                        
                        - Allow tap to click on charts. The cool part about the map plot is how you can view
                        metadata about the show if you hover over it. However, this only works
                        on web right now. I hope to make this available on mobile with a tap.
                        
                        - Google analytics integration. I want to see how many people are using the site and
                        where they're from.
                        
                        - Users should be able to save results so they don't need to re-select shows every time
                        they use the site. Until I fix that, I apologize for the inconvenience.
                        
                        - Probably other stuff
                        
                        If anyone wants to assist on any of this, please reach out at bkmurphy5@gmail.com!
                        """
                        )
                    ],
                    title="What are some current issues you're working on?",
                ),
            ],
        ),
    ]
)
