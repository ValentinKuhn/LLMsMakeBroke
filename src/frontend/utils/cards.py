
import dash
from dash import html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc


user_prompts = dbc.Card([
    dbc.CardHeader("User Prompts"),
    dbc.CardBody([dbc.Row([
        dbc.Col(
            [dbc.Row([
                html.H4(
                    "Do you add context to the user prompt e.g. with RAG"),
                html.H5(
                    "e.g. one additional pdf page is roughly 200 tokens"),
                dcc.Input(id='input-input_rag', type='number', className='custom-input',
                          placeholder='Average number of tokens per request...', style={"offset": 1}),
            ])]
        ),
        dbc.Col(width=1),
        dbc.Col(
            dbc.Row([html.H4("How long is the average prompt of a user?"),
                     html.H5(
                "'Provide me with the policy for work-at-home' is 11 token"),
                dcc.Input(id='input-input_tokens', type='number', className='custom-input',
                          placeholder='Average number of tokens per request...'),])
        ),])
    ]
    )
]
)

output_prompts = dbc.Card([
    dbc.CardHeader("Output Token"),
    dbc.CardBody([dbc.Row([
        dbc.Col(
            [dbc.Row([
                html.H4(
                    "How many tokens will the model return?"),
                html.H5(
                    "e.g. one token (yes/no), short description 50 tokens, long description 300 tokens"),
                dcc.Input(id='input-output_token', type='number', className='custom-input',
                          placeholder='Expected token per answer'),
            ])]
        ),
        dbc.Col(width=1),
        dbc.Col(
            dbc.Row([html.H4(""),
                     html.H5(
                ""),
            ])
        ),])
    ]
    )
]
)


input_prompts = dbc.Card([
    dbc.CardHeader("Output Token"),
    dbc.CardBody([dbc.Row([
        dbc.Col(
            [dbc.Row([
                html.H4("How many users do I have?"),
                html.H5(
                    "Average number of users over the month."),
                dcc.Input(id='input-input_user', type='number',
                          className='custom-input', placeholder='Average number of user...'),
            ])]
        ),
        dbc.Col(width=1),
        dbc.Col(
            dbc.Row([html.H4(
                "How often does one user interact with the LLM per day?"),
                html.H5(
                "Average user requests."),
                dcc.Input(id='input-input_amount', type='number', className='custom-input',
                          placeholder='Average number of requests per day...')
            ])
        ),])
    ]
    )
]
)
