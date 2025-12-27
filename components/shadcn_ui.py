from dash import html

def Card(children, title=None, description=None, className=""):
    header = []
    if title:
        header.append(html.H4(title, className="font-semibold text-lg tracking-tight text-slate-900"))
    if description:
        header.append(html.P(description, className="text-sm text-slate-500 mt-1"))

    return html.Div([
        html.Div(header, className="flex flex-col space-y-1.5 p-6 pb-4") if header else None,
        html.Div(children, className="p-6 pt-0 flex-1")
    ], className=f"rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md {className}")