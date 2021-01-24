import psycopg2
import re
from tiling.tiler import Tiler
from dotenv import load_dotenv
import os

def get_unprocessed_panos(conn):
    p = re.compile(r'[\d\-\.]+')
    cur = conn.cursor()
    cur.execute("SELECT id,ST_AsText(the_geom) FROM panoramas WHERE ele IS NULL ORDER BY id")
    results = cur.fetchall()
    cur.close()
    new_results = []
    for result in results:
        nums = [float(n) for n in p.findall(result[1])]
        new_results.append((result[0], (nums[0], nums[1])))
    return new_results
   
def add_elevation(conn, panos):
    tiler = Tiler("https://hikar.org/webapp/proxy.php?x={x}&y={y}&z={z}")
    cur = conn.cursor()
    for pano in panos:
        sphmerc_coords = tiler.sphMerc.project(pano[1])
        dem = tiler.getData(sphmerc_coords)
        ele = int(dem.getHeight(sphmerc_coords))
        cur.execute("UPDATE panoramas SET ele=%s WHERE id=%s", (ele, pano[0]))
        print(f"Pano #{pano[0]} has ele {ele}m")
    conn.commit()
    cur.close()
            
def main():
    load_dotenv()
    conn = psycopg2.connect(f"dbname={os.environ.get('DB_NAME')} user={os.environ.get('DB_USER')}")
    panos = get_unprocessed_panos(conn)
    add_elevation(conn, panos)
    conn.close()

if __name__ == "__main__":
    main()
