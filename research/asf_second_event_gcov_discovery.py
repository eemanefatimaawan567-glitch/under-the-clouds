# ASF NISAR GCOV second-event candidate scene DISCOVERY (metadata only)
# Install: pip install -U asf_search pandas
# This does not establish flooding or independent external-event validation.
import asf_search as asf
import pandas as pd

AOIS={
 "Dadu_Sindh_research_box":(67.60,26.65,67.95,26.95),
 "Dera_Ghazi_Khan_research_box":(70.10,29.90,70.50,30.25),
}
def wkt(bounds):
    w,s,e,n=bounds
    return f"POLYGON(({w} {s},{e} {s},{e} {n},{w} {n},{w} {s}))"

rows=[]
for name,box in AOIS.items():
    try:
        matches=asf.search(dataset="NISAR",processingLevel="GCOV",
          intersectsWith=wkt(box),start="2026-06-01T00:00:00Z",
          end="2026-11-15T00:00:00Z",maxResults=250)
    except Exception as e:
        print("Query failed:",name,str(e))
        continue
    print(name,":",len(matches),"catalog items (limit 250; not exhaustive)")
    for scene in matches:
        p=scene.properties
        rows.append(dict(area=name,scene_name=p.get("sceneName"),
           date=p.get("startTime"),orbit=p.get("pathNumber"),
           frame=p.get("frameNumber"),direction=p.get("flightDirection"),
           polarization=str(p.get("polarization")),url=p.get("url")))
out=pd.DataFrame(rows)
out.to_csv("ASF_SECOND_EVENT_NISAR_SCENE_CANDIDATES.csv",index=False)
print(out.to_string(index=False))
print("NO EXTERNAL FLOOD VALIDATION HAS BEEN PERFORMED.")
print("For a real second-event test, obtain dated before/after matching GCOV scenes,")
print("an independently documented event and coverage/labels, then apply locked model.")
