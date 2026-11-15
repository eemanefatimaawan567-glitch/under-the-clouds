# Terrapulse — Sentinel-2 independent optical evidence screening for GPS targets
# Run in Google Colab. Uses Earth Engine project undertheclouds-nisar.
# Independent *optical signal* is not independent field-confirmed flooding.
from google.colab import drive
drive.mount('/content/drive')
import ee, pandas as pd, numpy as np, json
from pathlib import Path
try: ee.Initialize(project='undertheclouds-nisar')
except Exception:
    ee.Authenticate()
    ee.Initialize(project='undertheclouds-nisar')
base=Path('/content/drive/MyDrive/UnderTheClouds/jatoi/original_subset')
out=base/'flood_validation_upgrade'/'independent_optical_audit'
out.mkdir(parents=True,exist_ok=True)
gpsfile=base/'flood_validation_upgrade'/'TERRAPULSE_INTERIOR_CLUSTERS_GPS.csv'
gps=pd.read_csv(gpsfile).head(10)
required={'latitude','longitude'}
assert required.issubset(gps.columns), f'Expected {required} in GPS CSV'
windows={'before':('2026-08-01','2026-08-13'),'after':('2026-09-04','2026-09-16')}
def inspect(lat,lon,start,end):
    pt=ee.Geometry.Point([float(lon),float(lat)])
    area=pt.buffer(60)
    col=ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(pt).filterDate(start,end).sort('system:time_start')
    n=int(col.size().getInfo())
    if not n:return []
    def examine(im):
        im=ee.Image(im)
        scl=im.select('SCL')
        clear=(scl.eq(4).Or(scl.eq(5)).Or(scl.eq(6))).rename('clear')
        water=scl.eq(6).rename('water').updateMask(clear)
        mndwi=im.normalizedDifference(['B3','B11']).rename('mndwi').updateMask(clear)
        kw=dict(geometry=area,scale=20,maxPixels=100000,bestEffort=True)
        return ee.Feature(None,{'scene_id':im.get('system:index'),
            'date_ms':im.get('system:time_start'),
            'local_clear':clear.reduceRegion(reducer=ee.Reducer.mean(),**kw).get('clear'),
            'water_fraction_clear':water.reduceRegion(reducer=ee.Reducer.mean(),**kw).get('water'),
            'mndwi_median':mndwi.reduceRegion(reducer=ee.Reducer.median(),**kw).get('mndwi')})
    return [f['properties'] for f in ee.FeatureCollection(
        ee.List(col.toList(n)).map(lambda item:examine(ee.Image(item)))).getInfo()['features']]
all_rows=[]; selected=[]
for i,row in gps.reset_index(drop=True).iterrows():
    for period,(start,end) in windows.items():
        print('Checking target',i+1,period)
        found=inspect(row.latitude,row.longitude,start,end)
        for scene in found:all_rows.append(dict(target=i+1,period=period,**scene))
        good=[x for x in found if x.get('local_clear') is not None and x['local_clear']>=.8 and x.get('mndwi_median') is not None]
        best=sorted(good,key=lambda x:(-x['local_clear'],x['date_ms']))[0] if good else {}
        selected.append(dict(target=i+1,period=period,scene_count=len(found),status='CLEAR' if good else 'INCONCLUSIVE_NO_CLEAR_SCENE',**best))
pd.DataFrame(all_rows).to_csv(out/'all_scene_provenance.csv',index=False)
s=pd.DataFrame(selected);s.to_csv(out/'selected_scene_provenance.csv',index=False)
results=[]
for i in range(1,len(gps)+1):
    b=s[(s.target==i)&(s.period=='before')].iloc[0]
    a=s[(s.target==i)&(s.period=='after')].iloc[0]
    status='INCONCLUSIVE'
    if b.status=='CLEAR' and a.status=='CLEAR':
        if b.mndwi_median<=0 and b.water_fraction_clear<=.1 and a.mndwi_median>=.15 and a.water_fraction_clear>=.4:
            status='OPTICAL_WATER_CHANGE_SIGNAL_NOT_FIELD_PROOF'
        elif b.mndwi_median>=.15 or b.water_fraction_clear>=.4:
            status='BEFORE_ALREADY_WATER_LIKE'
        else:status='NO_STRICT_OPTICAL_CHANGE_EVIDENCE'
    results.append(dict(target=i,latitude=gps.iloc[i-1].latitude,longitude=gps.iloc[i-1].longitude,
        before_scene=b.get('scene_id'),after_scene=a.get('scene_id'),status=status,field_confirmed=False))
result=pd.DataFrame(results)
result.to_csv(out/'exact_gps_optical_status.csv',index=False)
display(result)
# Separate event validation is NOT completed without independent NISAR before/after scenes and labels.
second=dict(status='NOT_TESTED_MISSING_SECOND_EVENT_NISAR_AND_REFERENCE',
    external_event_field_accuracy_claimed=False)
(out/'second_event_status.json').write_text(json.dumps(second,indent=2))
print('OUTPUTS:',out)
print('Optical result != verified ground flood. Another-event validation NOT TESTED.')
