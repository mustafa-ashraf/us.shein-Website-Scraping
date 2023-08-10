import requests
from bs4 import BeautifulSoup
import csv
import os
    
Main_category = "Women"
women_sub_category = ["Dresses","Tops","Beachwear","Jumpsuits-and-Two-piece","Denim","lingerie & longuewear","bottoms","active wear","acc-jewelry","shoes-bags"]
women_sub_categories_urls=["https://us.shein.com/Women-Dresses-c-1727.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_1%60ps%3D4_1%60jc%3Dreal_1727&src_tab_page_id=page_home1682696836824&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-1_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/Women-Tops-c-2223.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_2%60ps%3D4_2%60jc%3Dreal_2223&src_tab_page_id=page_home1682698211177&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-2_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/Women-Beachwear-c-2039.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_3%60ps%3D4_3%60jc%3Dreal_2039&src_tab_page_id=page_home1682698249374&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-3_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/recommend/Jumpsuits-and-Two-piece-sc-10066905.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_4%60ps%3D4_4%60jc%3DitemPicking_10066905&src_tab_page_id=page_home1682698269324&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-4_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/Women-Denim-c-1930.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_5%60ps%3D4_5%60jc%3Dreal_1930&src_tab_page_id=page_home1682698284922&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-5_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/recommend/Underwear-Sleepwear-sc-100116123.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_13%60ps%3D4_9%60jc%3DitemPicking_100116123&src_tab_page_id=page_home1682698301019&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-9_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/Women-Bottoms-c-1767.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_8%60ps%3D4_6%60jc%3Dreal_1767&src_tab_page_id=page_home1682698321672&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-6_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/category/Sports-and-Outdoors-sc-008120532.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_9%60ps%3D4_7%60jc%3DitemPicking_008120532&src_tab_page_id=page_home1682698337863&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-7_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/promotion/us-women-acc-jewelry-sc-025114684.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_10%60ps%3D4_8%60jc%3DitemPicking_025114684&src_tab_page_id=page_home1682698365373&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-8_ABT%3DSPcCccWomenHomepage_expgroup_100004156",
                           "https://us.shein.com/promotion/us-shoes-bags-sc-02577097.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_14%60ps%3D4_10%60jc%3DitemPicking_02577097&src_tab_page_id=page_home1682698381726&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D3743529_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-10_ABT%3DSPcCccWomenHomepage_expgroup_100004156"]

main_category_list = []
sku_url = []
sub_category = []
for x in range(len(women_sub_categories_urls)):
    print(women_sub_category[x])
    page = 1  
    while True:
        # Get the HTML of the target website
        response = requests.get(women_sub_categories_urls[x] + "&page=" + str(page))
        soup = BeautifulSoup(response.content, "html.parser")
        divs = soup.findAll("section", class_="S-product-item")
        
        if len(divs) == 0:
            break  # Break the loop if there are no more products on the page
        
        for f in divs:
            sku_url.append("https://us.shein.com" + str(f.find("a")['href']))
            main_category_list.append(Main_category)
            sub_category.append(women_sub_category[x])
        
        page += 1
        
        
import pandas as pd
df = pd.DataFrame(main_category_list,columns=["Main category"])
df["sub_category"] = sub_category
df["sku_url"] = sku_url
df.to_csv("Urls.csv",index=False)