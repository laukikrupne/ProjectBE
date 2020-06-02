import os
import requests
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
import json
import numpy as np
import cv2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists


'''inf_dict = {            "Apple___Apple_scab":{
                                                "title":"Apple Scrab",
                                                "caused_by":"Fungus Venturia Inaequalis",
                                                "desc":"A serious disease of apples and ornamental crabapples, apple scab (Venturia inaequalis) attacks both leaves and fruit. The fungal disease forms pale yellow or olive-green spots on the upper surface of leaves. Dark, velvety spots may appear on the lower surface.",
                                                "treatment":"Choose resistant varieties when possible. Rake under trees and destroy infected leaves to reduce the number of fungal spores available to start the disease cycle over again next spring. Water in the evening or early morning hours (avoid overhead irrigation) to give the leaves time to dry out before infection can occur. Spread a 3- to 6-inch layer of compost under trees, keeping it away from the trunk, to cover soil and prevent splash dispersal of the fungal spores. For best control, spray liquid copper soap early, two weeks before symptoms normally appear. Alternatively, begin applications when disease first appears, and repeat at 7 to 10 day intervals up to blossom drop. Bonide® Sulfur Plant Fungicide, a finely ground wettable powder, is used in pre-blossom applications and must go on before rainy or spore discharge periods. Apply from pre-pink through cover (2 Tbsp/ gallon of water), or use in cover sprays up to the day of harvest. Organocide® Plant Doctor is an earth-friendly systemic fungicide that works its way through the entire plant to combat a large number of diseases on ornamentals, turf, fruit and more. Apply as a soil drench or foliar spray (3-4 tsp/ gallon of water) to prevent and attack fungal problems. Containing sulfur and pyrethrins, Bonide® Orchard Spray is a safe, one-hit concentrate for insect attacks and fungal problems. For best results, apply as a protective spray (2.5 oz/ gallon) early in the season. If disease, insects or wet weather are present, mix 5 oz in one gallon of water. Thoroughly spray all parts of the plant, especially new shoots."       
                                                }, 
                          "Apple___Black_rot":{
                                                "title":"Apple Black Rot",
                                                "caused_by":"fungus Xylaria: X. mail and X. polymorpha.",
                                                "desc":"Black root rot, also called dead man’s fingers or Xylaria root rot, is occasionally observed on mature apple and cherry trees. Although trees of all ages can be infected, most trees that die from black root rot are at least 10 years old .",
                                                "treatment":"Prune out cankers, dead branches, twigs, etc.... Prune and remove cankers at least 15 inches below the basal end; properly dispose of prunings by burial or burning. Remove all mummified fruit. Control fire blight by pruning out infected wood or controlling insect vectors."       
                                                },
                          "Apple___Cedar_apple_rust":{
                                                "title":"Apple Cedar / Apple Rust",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Apple___healthy":{
                                                "title":"Apple Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY",
                                                "treatment":"HEALTHY"       
                                                },
                          "Blueberry___healthy":{
                                                "title":"Blueberry Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY",
                                                "treatment":"HEALTHY."       
                                                },
                          "Cherry_(including_sour)___Powdery_mildew":{
                                                "title":"Cherry (including sour) Powdery Mildew",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Cherry_(including_sour)___healthy":{
                                                "title":"Cherry (including sour) Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY.",
                                                "treatment":"HEALTHY."       
                                                },
                          "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot":{
                                                "title":"Cercospora Leaf Spot / Grey Leaf Spot",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Corn_(maize)___Common_rust_":{
                                                "title":"Corn (maize) Common Rust",
                                                "caused_by":"Fungus Puccinia Sorghi",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"Destruction of plant debris by deep ploughing and other methods. Seed treatment with Metalaxyl at 4 g/kg and foliar spray of Mancozeb 2.5 g/l or Metalaxyl MZ at 2g/l is recommended. Use of resistant varieties like DMR 1, DMR 5 and Ganga 11."       
                                                
                                                
                                                },
                          "Corn_(maize)___Northern_Leaf_Blight":{
                                                "title":"Corn (maize) Northern Leaf Blight",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Corn_(maize)___healthy":{
                                                "title":"Corn (maize) Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY.",
                                                "treatment":"HEALTHY."       
                                                },
                          "Grape___Black_rot":{
                                                "title":"Grape Black Rot",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Grape___Esca_(Black_Measles)":{
                                                "title":"Grape Esca (Black Measles)",
                                                "caused_by":"Phaeomoniella chlamydospora and Phaeoacremonium aleophilum.",
                                                "desc":"Grapevine measles, also called esca, black measles or Spanish measles, has long plagued grape growers with its cryptic expression of symptoms and, for a long time, a lack of identifiable causal organism(s). The name measles refers to the superficial spots found on the fruit.",
                                                "treatment":"Spray every 14 days with Bonide® Fruit Tree Spray as a preventative measure. No more than 2 applications per year. Do not use more than 2 quarts of spray suspension per 100 square feet of grape vine."       
                                                
                                                
                                                },
                          "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)":{
                                                "title":"Grape Leaf Blight (Isariopsis Leaf Spot)",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Grape___healthy":{
                                                "title":"Grape Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY.",
                                                "treatment":"HEALTHY."       
                                                },
                          "Orange___Haunglongbing_(Citrus_greening)":{
                                                "title":"Orange Haunglongbing (Citrus Greening)",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Peach___Bacterial_spot":{
                                                "title":"Peach Bacterial Spot",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Peach___healthy":{
                                                "title":"Peach Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY.",
                                                "treatment":"HEALTHY."       
                                                },
                          "Pepper,_bell___Bacterial_spot":{
                                                "title":"Pepper Bell Bacterial Spot",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Pepper,_bell___healthy":{
                                                "title":"Pepper Bell Healthy",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Potato___Early_blight":{
                                                "title":"Potato Early Blight",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                
                                                
                                                },
                          "Potato___Late_blight":{
                                                "title":"Potato Late Blight",
                                                "caused_by":"fungus-like organism Phytophthora infestans",
                                                "desc":"The disease apparently originated in Mexico from where it spread, along with the potato, which spreads rapidly in the foliage of potatoes and tomatoes causing collapse and decay. The disease spreads most readily during periods of warm and humid weather with rain",
                                                "treatment":"Use potato tubers for seed from disease-free areas to ensure that the pathogen is not carried through seed tuber. The infected plant material in the field should be properly destroyed. Grow resistant varieties like Kufri Navtal. Fungicidal sprays on the appearance of initial symptoms."       
                                                
                                                
                                                },
                          "Potato___healthy":{
                                                "title":"Potato Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY.",
                                                "treatment":"HEALTHY."       
                                                },
                          "Raspberry___healthy":{
                                                "title":"Raspberry Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY.",
                                                "treatment":"HEALTHY."       
                                                },
                          "Soybean___healthy":{
                                                "title":"Soyabean Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY.",
                                                "treatment":"HEALTHY."       
                                                },
                          "Squash___Powdery_mildew":{
                                                "title":"Squash Powdery Mildew",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Strawberry___Leaf_scorch":{
                                                "title":"Strawberry Leaf Scorch",
                                                "caused_by":"Fungus Diplocarpon Earliana.",
                                                "desc":"Apply sulfur sprays or copper-based fungicides weekly at first sign of disease to prevent its spread. These organic fungicides will not kill leaf spot, but prevent the spores from germinating. Safely treat most fungal and bacterial diseases with SERENADE Garden..",
                                                "treatment":"During stretches of sunny, hot, and dry days, water your tree deeply. Lock in soil moisture by mulching your tree. Fertilize trees regularly to provide needed nutrients."       
                                                },
                          "Strawberry___healthy":{
                                                "title":"Strawberry Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY",
                                                "treatment":"HEALTHY"       
                                                },
                          "Tomato___Bacterial_spot":{
                                                "title":"Tomato Bacterial Spot",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Tomato___Early_blight":{
                                                "title":"Tomato Early Blight",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Tomato___Late_blight":{
                                                "title":"Tomato Late Blight",
                                                "caused_by":"fungus-like oomycete pathogen Phytophthora infestans.",
                                                "desc":"Late blight of potatoes and tomatoes, the disease that was responsible for the Irish potato famine in the mid-nineteenth century, which spreads rapidly in the foliage of potatoes and tomatoes causing collapse and decay. The disease spreads most readily during periods of warm and humid weather with rain.",
                                                "treatment":"Plant resistant cultivars when available. Remove volunteers from the garden prior to planting and space plants far enough apart to allow for plenty of air circulation. Water in the early morning hours, or use soaker hoses, to give plants time to dry out during the day — avoid overhead irrigation."       
                                                },
                          "Tomato___Leaf_Mold":{
                                                "title":"Tomato Leaf Mold",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Tomato___Septoria_leaf_spot":{
                                                "title":"Tomato Septoria Leaf Spot",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Tomato___Spider_mites Two-spotted_spider_mite":{
                                                "title":"Tomato Spider Mites / Two Spotted Spider Mite",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Tomato___Target_Spot":{
                                                "title":"Tomato Target Spot",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Tomato___Tomato_Yellow_Leaf_Curl_Virus":{
                                                "title":"Tomato Yellow Leaf Curl Virus",
                                                "caused_by":"This virus is transmitted by an insect vector from the family Aleyrodidae and order Hemiptera, the whitefly  Bemisia tabaci , commonly known as the silverleaf whitefly or the sweet potato whitefly.",
                                                "desc":"Tomato yellow leaf curl virus (TYLCV) is a DNA virus from the genus  Begomovirus  and the family  Geminiviridae . TYLCV causes the most destructive disease of tomato, and it can be found in tropical and subtropical regions causing severe economic losses. This virus is transmitted by an insect vector from the family Aleyrodidae and order Hemiptera, the whitefly  Bemisia tabaci , commonly known as the silverleaf whitefly or the sweet potato whitefly. The primary host for TYLCV is the tomato plant, and other plant hosts where TYLCV infection has been found include eggplants, potatoes, tobacco, beans, and peppers. Due to the rapid spread of TYLCV in the last few decades, there is an increased focus in research trying to understand and control this damaging pathogen. Some interesting findings include virus being sexually transmitted from infected males to non-infected females (and vice versa), and an evidence that TYLCV is transovarially transmitted to offspring for two generations.",
                                                "treatment":"Currently, the most effective treatments used to control the spread of TYLCV are insecticides and resistant crop varieties. The effectiveness of insecticides is not optimal in tropical areas due to whitefly resistance against the insecticides; therefore, insecticides should be alternated or mixed to provide the most effective treatment against virus transmission. Developing countries experience the most significant losses due to TYLCV infections due to the warm climate as well as the expensive costs of insecticides used as the control strategy. Other methods to control the spread of TYLCV include planting resistant/tolerant lines, crop rotation, and breeding for resistance of TYLCV. As with many other plant viruses, one of the most promising methods to control TYLCV is the production of transgenic tomato plants resistant to TYLCV."       
                                                },
                          "Tomato___Tomato_mosaic_virus":{
                                                "title":"Tomato Mosaic Virus",
                                                "caused_by":"Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "desc":"Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) .",
                                                "treatment":"The fungus attacks leaves and twigs, producing symptoms much like powdery mildew on apples. Infected leaves curl upward. Newly developed leaves on new shoot growth become progressively smaller, are generally pale, and are somewhat distorted. New shoots are shorter in length than normal. By mid-season, the whitish fungus can be seen growing over the leaves and shoots, sometimes in patches and other times covering most of the new growth. Such symptoms are especially common in nursery trees. The growth of sour cherry trees in the nursery and in young orchards is reduced by this disease."       
                                                },
                          "Tomato___healthy":{
                                                "title":"Tomato Healthy",
                                                "caused_by":"Nothing.",
                                                "desc":"HEALTHY",
                                                "treatment":"HEALTHY"       
                                                }
                        }'''
db_url = 'mysql+pymysql://root:root@mysql/plant_deficiency'
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
DEBUG = True
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# create database if not exists
if not database_exists(db_url):
    create_database(db_url)

class Deficiency(db.Model):
    Deficiency = db.Column(db.VARCHAR(55), primary_key=True)
    title = db.Column(db.VARCHAR(55))
    caused_by = db.Column(db.Text)
    desc = db.Column(db.Text)
    treatment = db.Column(db.Text)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

url = "http://api:8000/plant_deficiency" 

content_type = 'image/jpeg'
headers = {'content-type': content_type}

@app.route('/' , methods=['GET', 'POST'])
def index():		
	return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files :
            flash('No file part')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filex = file.read()
            nparr = np.fromstring(filex, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            _, img_encoded = cv2.imencode('.jpg', img)
            # send http request with image and receive response
            r = requests.post(url, data=img_encoded.tostring(), headers=headers)
            y = r.json()
            zzz = y['Deficiency']
            #zzzz = inf_dict[zzz]
            #zzzz = Deficiency.select().where(deficiency.columns.deficiency == zzz)
            zzzz = Deficiency.query.filter_by(Deficiency=zzz).first()
            return render_template('def.html', string = zzzz)
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
	app.run(debug=True)