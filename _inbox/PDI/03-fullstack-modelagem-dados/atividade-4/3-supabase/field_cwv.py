import requests
def crux(url, key):
    r = requests.post("https://chromeuxreport.googleapis.com/v1/records:queryRecord",
                      params={"key": key}, json={"url": url, "formFactor": "DESKTOP"})
    m = r.json()["record"]["metrics"]
    return {k: m[k]["percentiles"]["p75"] for k in
            ("largest_contentful_paint", "interaction_to_next_paint", "cumulative_layout_shift")}
