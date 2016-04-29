from bs4 import BeautifulSoup
import requests


def matching_words(string_1, string_2):
    count = 0
    string_1 = string_1.split()
    
    for word in string_1:
        if word in string_2:
            count += 1
    return count
    
def good_match(string, num_matching_words):
    string = string.split()
    str_len = len(string)
    if str_len > 0:
        percent =(float(num_matching_words)*100/float(str_len))
        if percent >= 50:
            return True
    return False

def get_data(url):
    try:
        result      = requests.get(url)
        soup        = BeautifulSoup(result.text, "html.parser")
        thumbnails  = []
        title       = ""
        
        if "amazon.com" in url:
            soup_title  = soup.find("span",id="productTitle")
            soup_img    = soup.find_all("img", id="landingImage")
            
            if not soup_img:
                return {"error":1,"data":{},"message":"Unable to extract images."}
            else:
                for img in soup_img:
                    if img["src"] not in thumbnails:
                        thumbnails.append(img["src"])
                
                if soup_title:
                    title = soup_title.string

            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
        
        elif "ebay.com" in url:
            soup_title = soup.find("h1", id="itemTitle")
            soup_img = soup.find_all("img", id="icImg")
            
            if not soup_img:
                return {"error":1,"data":{},"message":"Unable to extract images."}
            else:
                for img in soup_img:
                    if img["src"] not in thumbnails:
                        thumbnails.append(img["src"])
                
                if soup_title:
                    children = []
                    for child in soup_title.children:
                        children.append(child)
                    title = children[1]

            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
        
        else:
            title = soup.title.string
            for img in soup.find_all("img", alt=True):
                alt = img['alt']
                src = img['src']
                numMatchingWords = matching_words(title,alt)
                if good_match(alt, numMatchingWords):
                    if src not in thumbnails and src[-4:]==".jpg" and "sprite" not in src:
                        thumbnails.append(src)
            
            if not thumbnails:
                for img in soup.findAll("img", src=True):
                    if "sprite" not in img["src"] and src[-4:]==".jpg":
                        thumbnails.append(img["src"])
            
            if not thumbnails:
                return {"error":1,"data":{},"message":"Unable to extract images."}
    
            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
    
    except requests.exceptions.RequestException:
        return {"error":2,"data":{},"message":"URL entered is invalid."}
    
    

url1 = "http://www.amazon.com/PB278Q-2560x1440-DisplayPort-Ergonomic-Back-lit/dp/B009C3M7H0/ref=pd_sim_147_6?ie=UTF8&dpID=41kIGw387wL&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&refRID=15TJ4Q65C6BQWS8MNARZ"
url2 = "http://www.ebay.com/itm/Unlocked-Dual-Sim-BLU-PHONE-Advance-5-0-Smartphone-US-GSM-White-/262304395053?hash=item3d128f6f2d:g:ntQAAOSwe7BWzOQU"
url3 = "http://www.amazon.com/gp/product/B00THKEKEQ/ref=s9_ri_gw_g421_i1_r?ie=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-4&pf_rd_r=1WEK74K6Y8MXQC6BSHDN&pf_rd_t=36701&pf_rd_p=2437869562&pf_rd_i=desktop"
url4 = "http://www.amazon.com/gp/product/B012GC5DX8/ref=s9_qpp_gw_d38_g107_i1_r?ie=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-1&pf_rd_r=0HX3HCEVK96HB5FDXMV0&pf_rd_t=36701&pf_rd_p=2437869742&pf_rd_i=desktop"
url5 = "http://www.forever21.com/Product/Product.aspx?BR=f21&Category=dress&ProductID=2000187141&VariantID="
url6 = "http://www.homedepot.com/p/Samsung-Chef-Collection-24-1-cu-ft-4-DoorFlex-French-Door-Refrigerator-in-Stainless-Steel-Counter-Depth-RF24J9960S4/206046683"
url7 = "http://www.amazon.com/Cable-Matters-DisplayPort-Thunderbolt-Compatible/dp/B00ESM3CGA/ref=pd_sim_147_1?ie=UTF8&dpID=31yhLpt33sL&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&refRID=08DN5S05SEHHQ7XA7CRR"
url8 = "http://www.amazon.com/dp/B01CX26VNC/ref=s9_acsd_bw_wf_a_NREsmgwt_cdl_0?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=0XTGA18041VSCZS731HX&pf_rd_t=101&pf_rd_p=7dd8b26a-ae49-427d-8df0-4ddd3da6a98e&pf_rd_i=14045457011"
