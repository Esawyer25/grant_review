
import django
import os
import sys

PATH=os.path.abspath(os.path.dirname(__file__))

if os.name == 'posix': # Unix based systems
    bin_name = 'bin'
else:                  # Windows
    bin_name = 'Scripts'

# Relative path to the virtual environment
# (relative to the stand-alone script)
rel_path = '../venv/%s/activate_this.py' % bin_name
activate_this = os.path.join(PATH, rel_path)

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CapProj.settings")

django.setup()
from django.core.exceptions import ValidationError
from CapApp.models import Publication, Grant_Publication, Grant
from CapApp.custom_classes import Score, Publication_methods, Stats

STRING1 = "Nearly Ten Years Passed Since Dursleys Woken Nephew Front Step Privet Drive Hardly Changed Sun Rose Same Tidy Front Gardens Lit Brass Four Dursleys' Front Door Crept Living Room Almost Exactly Same Night Mr Dursley Seen Fateful News Report Owls Only Photographs Mantelpiece Really Showed Much Passed Ten Years Ago Lots Pictures Looked Large Pink Beach Ball Wearing Different-colored Bonnets - Dudley Dursley Longer Baby Photographs Showed Large Blond Boy Riding Bicycle Carousel Fair Playing Computer Game Father Being Hugged Kissed Mother Room Held Sign Another Boy Lived House Too Yet Harry Potter Still Asleep Moment Aunt Petunia Awake Shrill Voice Noise Dressed Went Hall Kitchen Table Almost Hidden Beneath Dudley's Birthday Presents Looked Though Dudley Gotten New Computer Wanted Mention Second Television Racing Bike Exactly Dudley Wanted Racing Bike Mystery Harry Dudley Fat Hated Exercise - Unless Course Involved Punching Somebody Dudley's Favorite Punching Bag Harry Couldn't Often Catch Harry Didn't Fast Perhaps Something Living Dark Cupboard Harry Always Small Skinny Age Looked Even Smaller Skinnier Really Because Wear Old Clothes Dudley's Dudley Four Times Bigger Harry Thin Face Knobbly Knees Black Hair Bright Green Eyes Wore Round Glasses Held Together Lot Scotch Tape Because Times Dudley Punched Nose Only Thing Harry Liked Own Appearance Thin Scar Forehead Shaped Bolt Lightning Remember Question Ever Remember Asking Aunt Petunia Gotten"

STRING2 = "Harry Staring Plate Funny Ringing Ears Grasp Broom Firmly Tail Thought Couldn't Remember Came Next Aunt Marge's Voice Seemed Boring Uncle Vernon's Drills Uncle Vernon Aunt Petunia Looking Extremely Tense Dudley Even Looked Pie Gape Parents Aunt Marge Suddenly Stopped Speaking Moment Looked Though Words Failed Seemed Swelling Inexpressible Angerswelling Didn't Stop Great Red Face Started Expand Tiny Eyes Bulged Mouth Stretched Too Tightly Speechnext Second Several Buttons Just Burst Tweed Jacket Pinged Off Wallsinflating Monstrous Balloon Stomach Bursting Free Tweed Waistband Fingers Blowing Salami Uncle Vernon Seized Marge's Feet Tried Pull Again Almost Lifted Floor Himself Second Later Ripper Leapt Forward Sank Teeth Uncle Vernons Legharry Tore Dining Room Before Anyone Stop Heading Cupboard Under Stairs Cupboard Door Burst Magically Open Reached Seconds Heaved Trunk Front Door Sprinted Upstairs Threw Himself Under Bed Wrenching Loose Floorboard Grabbed Pillowcase Full Books Birthday Presents Wriggled Seized Hedwig's Empty Cage Dashed Back Downstairs Trunk Just Uncle Vernon Burst Dining Room Trouser Leg Bloody Tattersbut Reckless Rage Harry Kicked Trunk Open Pulled Wand Pointed Uncle Vernonand Next Moment Dark Quiet Street Heaving Heavy Trunk Behind Hedwig's Cage Under Arm"

cleaned_string1 = Stats.remove_common_words(STRING1)
cleaned_string2 = Stats.remove_common_words(STRING2)
print (cleaned_string1)
print()
print(cleaned_string2)


###random grants paired with random abstracts


random_publications =  Grant_Publication.objects.filter(project_number__startswith="R01").order_by('?')[:20]

# random_publications = random_publications.filter(project_number__startswith="R01")

number = random_publications.count()

random_grants =  Grant.objects.filter(activity="R01").order_by('?')[:20]

pubs = Publication_methods.return_list_of_publications(random_publications)

index = 0
random_score = [31.0322412983658, 35.81898937714463, 39.25557285278104, 28.0, 34.942810419312295, 26.94438717061496, 39.96248240537617, 36.0, 34.26368339802363, 38.63935817272331, 29.597297173897484, 36.38681079732051, 20.322401432901575, 33.57082066318904, 31.0, 36.701498607005135, 32.7566787083184, 28.861739379323623, 38.54867053479276, 28.827070610799147, 41.27953488110059, 33.94112549695428, 36.29049462324811, 29.359836511806396, 32.01562118716424, 32.32645975048923, 28.124722220850465, 20.248456731316587, 36.9729630946723, 38.31448812133603, 29.478805945967352, 29.274562336608895, 18.894443627691185, 33.689761055846034, 30.463092423455635, 25.84569596664017, 31.096623610932426, 35.04283093587046, 31.28897569432403, 34.79942528261063, 35.12833614050059, 29.8496231131986, 28.284271247461902, 20.174241001832016, 31.448370387032774, 31.52776554086889, 38.36665218650175, 34.79942528261063, 34.95711658589707]

HP_score =[
30.789608636681304, 33.61547262794322, 36.4828726939094, 25.84569596664017, 31.51190251317746, 27.331300737432898, 39.698866482558415, 34.79942528261063, 37.52332607858744, 40.0374824383352, 32.61901286060018, 33.1058907144937, 27.60434748368452, 32.83291031876401, 28.792360097775937, 36.945906403822335, 36.89173349139343, 32.32645975048923, 41.83300132670378, 30.854497241083024, 43.289721643826724, 30.44667469527666, 38.39270764090493, 33.94112549695428, 33.95585369269929, 32.55764119219941, 29.9833287011299, 21.93171219946131, 37.86819245752297, 38.66522985836241, 31.080540535840107, 32.218007387174026, 25.45584412271571, 33.15116890850155, 31.096623610932426, 31.20897306865447, 32.18695387886216, 36.30426972134269, 34.741905532080416, 36.02776706930364, 36.40054944640259, 32.41913015489465, 32.57299494980466, 22.847319317591726, 34.27827300200522, 36.959437225152655, 37.403208418530085, 36.193922141707716, 37.82856063875548]

for pub in pubs:
    # if random_grants[index].abstract_text == None or pub.abstract == "":
    #     pass
    # else:
    if random_grants[index].abstract_text == "":
        pass
    else:
        if pub.abstract == "":
            pass
        else:
            cleaned_grantab_text = Stats.remove_common_words(random_grants[index].abstract_text)

            cleaned_paperab_text = Stats.remove_common_words(pub.abstract)
            print('---------------')
            print(f'CLEANED RANDOM GRANT:{cleaned_grantab_text}')
            print(f'CLEANED RANDOM PAPER: {cleaned_paperab_text}')
            print('---------------')
            random_score.append( Stats.euclidian(cleaned_grantab_text, cleaned_paperab_text))

            #compare to HP
            if index % 2 == 0:
                HP_score.append(Stats.euclidian(cleaned_grantab_text, cleaned_string1))
            else:
                HP_score.append(Stats.euclidian(cleaned_grantab_text, cleaned_string2))
    index += 0


##matched grants paired with matched abstracts
random_publications =  Grant_Publication.objects.filter(project_number__startswith="R01").order_by('?')[:50]

pubs = Publication_methods.return_list_of_publications(random_publications)

matched_score = []
print(random_publications)
for link in random_publications:
    try:
        matched_grant = Grant.objects.get(core_project_num = link.project_number)
    except:
        matched_grant = None
    print(f'matched_grant = {matched_grant}')

    if matched_grant:
        # Publication_methods.return_list_of_publications(link)
        pub = Publication.objects.get(pmid = link.pmid)

        if matched_grant.abstract_text == None or pub.abstract == "":
            pass
        else:
            cleaned_grantab_text = Stats.remove_common_words(matched_grant.abstract_text)
            cleaned_paperab_text = Stats.remove_common_words(pub.abstract)
            # print('---------------')
            # print(f'CLEANED MATCHED GRANT: {cleaned_grantab_text}')
            # print(f'CLEANED MATCHED PAPER: {cleaned_paperab_text}')
            # print('---------------')
            score = Stats.euclidian(cleaned_grantab_text, cleaned_paperab_text)
            matched_score.append(score)
            pub.score = round(score, 3)
            pub.save()
    else:
        "I can't find the matching grant"

print(f'these are the scores for random abstracts: {random_score}')
average = sum(random_score)/len(random_score)
print(f'average random score is {average}')
print("-------------")

print(f'these are the scores for HP: {HP_score}')
average = sum(HP_score)/len(HP_score)
print(f'average random score is {average}')
print("-------------")

print(f'these are the scores for matches: {matched_score}')
all_matches = Publication.objects.exclude(score = None)
total = 0
number_of_matches = 0
for match in all_matches:
    total += match.score
    if match.score:
        number_of_matches += 1
    else:
        pass

average = total/number_of_matches

print (number_of_matches)
print(f'average is {average}')
