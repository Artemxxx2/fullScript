import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import json
from bs4 import BeautifulSoup
import time
import mysql.connector
from dotenv import load_dotenv
import os
import json
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

# Expand cities list and grabs them
if os.path.exists('./citiesList.txt'):
    os.remove('./citiesList.txt')
if os.path.exists('./profiles.txt'):
    os.remove('./profiles.txt')
if os.path.exists('./uniqueProfiles.txt'):
    os.remove('./uniqueProfiles.txt')
    
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-features=NetworkService")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
service = Service(executable_path=os.getenv("EXECUTABLE_PATH"))


driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get('https://www.escortforumit.xxx/')
wait = WebDriverWait(driver, 15)  
wait.until(EC.presence_of_element_located((By.ID, 'show-more-btn')))
moreCities = driver.find_element(By.ID, 'show-more-btn') 
moreCities.click()

html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')

div_element = soup.find('div', class_='regions-list')

for div_element in div_element.find_all('ul'):
    for a_element in div_element.find_all('a'):
        link_url = a_element['href']
        with open('citiesList.txt' , 'a' ,encoding='utf-8') as file:
                file.write('https://www.escortforumit.xxx' + link_url + '\n')
# End of citiesList
# Grabs particular girl link

with open('citiesList.txt', 'r') as file:
    links = file.readlines()

for link in links:
    driver.get(link)
    wait = WebDriverWait(driver, 15)  
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'escorts-list')))
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    div_element = soup.find('div', class_='escorts-list')
    for element in soup.find_all('div', class_ = 'escort-item'):
        image_elements = element.find('div', class_='image')
        link_url = image_elements.find('a')
        url = link_url['href']
        with open('profiles.txt' , 'a' ,encoding='utf-8') as file:
            file.write('https://www.escortforumit.xxx' + url.replace(' ', '%20') + '\n')
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next = driver.find_element(By.CLASS_NAME, 'page-next')
        next.click()
        wait = WebDriverWait(driver, 15)  
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'escorts-list')))
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        div_element = soup.find('div', class_='escorts-list')
        for element in soup.find_all('div', class_ = 'escort-item'):
            image_elements = element.find('div', class_='image')
            link_url = image_elements.find('a')
            url = link_url['href']
            with open('profiles.txt' , 'a' ,encoding='utf-8') as file:
                file.write('https://www.escortforumit.xxx' + url.replace(' ', '%20') + '\n')
    except:
        pass

# #END Grabs particular girl link

# make unique
with open('profiles.txt', 'r') as file:
    links = file.readlines()
unique_set = set(links)
unique_list = list(unique_set)

for el in unique_list:
    with open('uniqueProfiles.txt' , 'a' ,encoding='utf-8') as file:
        file.write(el)
#END make unique

def forProc(link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    service = Service(executable_path=os.getenv("EXECUTABLE_PATH"))
    
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.get(link)
    bio = {}
    tariffs = {}
    incall = {}
    outcall = {}
    cityTour = {}
    tariffs['incall'] = incall
    tariffs['outcall'] = outcall
    contacts = {}
    aboutme = ''
    idGirl = ''
    try:
        result = re.search('\d{1,}$', link)
        if result:
            idGirl = result.group()
    except:
        pass
    
    bigJsonFile = {}
    bigJsonFile['id'] = idGirl
    bigJsonFile['name'] = ''
    bigJsonFile['message-bubble'] = ''
    bigJsonFile['bio'] = bio
    bigJsonFile['tariffs'] = tariffs
    bigJsonFile['contacts'] = contacts
    bigJsonFile['aboutme'] = aboutme
    bigJsonFile['cityTour'] = cityTour


    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        div_element = soup.find('div', class_='message-bubble').text.replace("\n", "")
        bigJsonFile['message-bubble'] = div_element
    except:
        pass
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        div_element = soup.find('h2', class_='showname').text.replace("\n", "")
        bigJsonFile['name'] = div_element
    except:
        pass
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        div_element = soup.find('div', class_='profile-info-container')
    except:
        pass
    try:
        for row in div_element.find_all('div', class_='row'):
            label_spans = row.find(['span'], class_='label').text.replace("\n", "")
            data = row.find_all(['span','div'], class_='value')[0].text.replace("\n", "")
            bio[label_spans] = data
    except:
        pass
    
    try:
        div_element = soup.find('div', class_='incall-rate') 
        rates = div_element.find('div', class_ = 'rates')
        for row in rates.findAll('span' , class_ = 'p-row'):
            timedev =  row.find_all('span' , class_='p-col')[0].text.replace("\n", "")
            incall[timedev] = row.find_all('span' , class_='p-col')[1].text.replace("\n", "")
    except:
        pass
    
    try:
        div_element = soup.find('div', class_='outcall-rate') 
        rates = div_element.find('div', class_ = 'rates')
        for row in rates.findAll('span' , class_ = 'p-row'):
            timedev =  row.find_all('span' , class_='p-col')[0].text.replace("\n", "")
            outcall[timedev] = row.find_all('span' , class_='p-col')[1].text.replace("\n", "")
    except:
        pass
    
    try:
        div_element = soup.find('div', class_='tour-info')
        row = div_element.find_all('div', class_='p-row')
        for col in row:
            cityTour[col.select('.p-col')[0].text.replace("\n", "")] = col.select('.p-col')[1].text.replace("\n", "")
    except:
        pass
    
    try:
        div_element = soup.find('div', class_='tour-city')
        el = div_element.find('a')
        cityTour['city'] = el.text.replace("\n", "")
    except:
        pass    
        
    try:
        div_element = soup.find('div', class_='profile-contact-container')
        info_list = div_element.find('div', class_='p-info-list')
    except:
        pass
    try:
        for row in info_list.find_all('div', class_='p-row'):
               contacts[row.select('.p-col')[0].text.replace("\n", "")] = row.select('.p-col')[1].text.replace("\n", " ")
    except:
        pass
    try:
        div_element = soup.find('div', class_='profile-bottom-sheet-container')
        left = div_element.find('div', class_='left-side')
        telefone = left.find('span')
        contacts['telefone'] = telefone.text
    except:
        pass
    try:
        about =  soup.select('[style*="grid-column: 1/-1"], [style*="word-break: break-word"]')[0]
        res = ''
        for p in about.find_all('p'):
            res += p.text
        bigJsonFile['aboutme'] = res
    except:
        pass
    if bigJsonFile['name'] == '':
        pass
    else:
        arr.append(bigJsonFile)
    
with open('uniqueProfiles.txt', 'r') as file:
    links = file.readlines()

arr = []
chunk_size = 5

with ThreadPoolExecutor(max_workers=5) as executor:
    for i in range(0, len(links), chunk_size):
        chunk = links[i:i + chunk_size]
        executor.map(forProc, chunk)

with open("output.json", "w",encoding='utf-8') as outfile:
    json.dump(arr, outfile, ensure_ascii=False, indent=4)

driver.quit()


with open('./output.json','r',encoding='utf-8') as file:
    variable = json.load(file)

newData = []
oldData = []
i = 0

for el in variable:
    print(i)
    i += 1
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            pass

    except mysql.connector.Error as err:
        print("Connection error:", err)
        break
    try:
         cursor = connection.cursor()

         param1 = el['id']

         query = "SELECT * FROM `wp_drts_entity_field_string` WHERE `field_name` = 'field_foreign_id' AND value = %s"
         cursor.execute(query, (param1, ))

         results = cursor.fetchall()
    except:
        print('problem with query')
        break
    try:
        dbId = results[0][2]
        el['localId'] = dbId
        oldData.append(el)
    except:
        newData.append(el)

    

with open("oldData.json", "w",encoding='utf-8') as outfile:
    json.dump(oldData, outfile, ensure_ascii=False, indent=4)

with open("newData.json", "w",encoding='utf-8') as outfile:
    json.dump(newData, outfile, ensure_ascii=False, indent=4)


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-features=NetworkService")
service = Service(executable_path=os.getenv("EXECUTABLE_PATH"))

driver = webdriver.Chrome(service=service,options=chrome_options)


def safe_get(dictionary, *keys, default=None):
    for key in keys:
        if isinstance(dictionary, dict) and key in dictionary:
            dictionary = dictionary[key]
        else:
            return default
    return dictionary

def moneySection(time,field,filedType):
    try:
        match = re.match(r"\d{1,}", safe_get(el, 'tariffs', filedType, time , default=None))
        priceField = driver.find_element(By.XPATH, field)
        driver.execute_script("arguments[0].scrollIntoView();", priceField)
        priceField.send_keys(match.group())
    except:
        pass

def round_to_nearest_multiple(n, multiple):
    remainder = n % multiple
    if remainder < multiple / 2:
        rounded = n - remainder
    else:
        rounded = n + (multiple - remainder)
    if rounded > 86100:
        rounded = 0
    return rounded

def selectDay(dayIt,dayEN,el,i):
    try:
        if dayIt in el['contacts']:
            if i != 0:
                dateInput = driver.find_element(By.CLASS_NAME ,'drts-entity-form-field-name-field-opening-hours')
                add =  dateInput.find_element(By.CLASS_NAME, 'drts-form-field-add')
                add.click()
            forClick = driver.find_element(By.XPATH, '//select[@name="drts[field_opening_hours][' + str(i) + '][day]"]')  
            driver.execute_script("arguments[0].scrollIntoView();", forClick) 
            select = Select(forClick)
            select.select_by_visible_text(dayEN)
            match = re.findall(r'(\d\d:\d\d){1,}',el['contacts'][dayIt])
            forValue1 = 0
            forValue2 = 0
            forValue1 = round_to_nearest_multiple(int(match[0][0:2]) * 12 * 300 + int(match[0][3:]) / 5 * 300,300)
            forValue2 = round_to_nearest_multiple(int(match[1][0:2]) * 12 * 300 + int(match[1][3:]) / 5 * 300,300)

            start = driver.find_element(By.XPATH, '//select[@name="drts[field_opening_hours][' + str(i) + '][start]"]')  
            end = driver.find_element(By.XPATH, '//select[@name="drts[field_opening_hours][' + str(i) + '][end]"]')
            selectStart = Select(start)
            selectEnd = Select(end)
            selectStart.select_by_value(str(int(forValue1)))
            selectEnd.select_by_value(str(int(forValue2)))
            return 1
        else:
            return 0
    except:
        return 0

def formInput(input,jsonData):
    try:
        login = driver.find_element(By.XPATH, input)
        driver.execute_script("arguments[0].scrollIntoView();", login)
        login.send_keys(jsonData)
    except:
        pass

def category(elemToSearch):
    try:
        checklist = driver.find_element(By.ID,'escorts_dir_catchecklist')
        driver.execute_script("arguments[0].scrollIntoView();", checklist) 
        checklist = driver.find_element(By.ID,'escorts_dir_catchecklist')
        if elemToSearch == 'russian':
            li = checklist.find_element(By.ID,"in-escorts_dir_cat-15")
            driver.execute_script("arguments[0].scrollIntoView();", li) 
            li.click()
        else:
            li = checklist.find_element(By.XPATH,"//*[contains(text(), '" + elemToSearch +"')]")
            driver.execute_script("arguments[0].scrollIntoView();", li) 
            li.click()
    except:
        pass
    


load_dotenv()

driver.get('https://e-scort.it/wp-admin/post-new.php?post_type=escorts_dir_ltg')

with open('./newData.json','r',encoding='utf-8') as file:
    variable = json.load(file)

# login section
wait = WebDriverWait(driver, 15)  
wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="login[username]"]')))
login = driver.find_element(By.XPATH, '//input[@name="login[username]"]')
login.send_keys(os.getenv("WORDPRESS_LOGIN"))
password = driver.find_element(By.XPATH, '//input[@name="login[password]"]')
password.send_keys(os.getenv("WORDPRESS_PASSWORD"))
btn = driver.find_element(By.XPATH, '//button[@name="login[login][submit]"]') 
btn.click()
# login section
# fill Form



    
for el in variable:
        
        driver.get('https://e-scort.it/wp-admin/post-new.php?post_type=escorts_dir_ltg')
        wait = WebDriverWait(driver, 15)  
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="post_title"]')))
        
        formInput('//input[@name="post_title"]',el['name'])
        formInput('//input[@name="drts[field_etnia][0]"]', safe_get(el, 'bio', 'Etnia', default=None))
        formInput('//input[@name="drts[field_nazionalita][0]"]', safe_get(el, 'bio', 'Nazionalità', default=None))
        formInput('//input[@name="drts[field_eta][0]"]', safe_get(el, 'bio', 'Età', default=None))
        formInput('//input[@name="drts[field_occhi][0]"]',safe_get(el, 'bio', 'Occhi', default=None))
        
        formInput('//input[@name="drts[field_capelli][0]"]',safe_get(el, 'bio', 'Capelli', default=None))
        formInput('//input[@name="drts[field_lunghezza_dei_capelli][0]"]', safe_get(el, 'bio', 'Lunghezza dei capelli', default=None))
        formInput('//input[@name="drts[field_peli_pubici][0]"]',safe_get(el, 'bio', 'Peli pubici', default=None))
    
        formInput('//input[@name="drts[field_altezza][0]"]', safe_get(el, 'bio', 'Altezza', default=None))
        formInput('//input[@name="drts[field_peso][0]"]',safe_get(el, 'bio', 'Peso', default=None))
        formInput('//input[@name="drts[field_busto_vita_fianchi][0]"]',safe_get(el, 'bio', 'Busto - Vita - Fianchi', default=None))
        formInput('//input[@name="drts[field_breast][0]"]',safe_get(el, 'bio', 'Breast', default=None))
    
        formInput('//input[@name="drts[field_coppa_taglia][0]"]', safe_get(el, 'bio', 'Coppa taglia', default=None))
        formInput('//input[@name="drts[field_misura_scarpe][0]"]',safe_get(el, 'bio', 'Misura scarpe', default=None))
    
        formInput('//input[@name="drts[field_taglia_del_vestito][0]"]', safe_get(el, 'bio', 'Taglia del vestito', default=None))
    
        formInput('//input[@name="drts[field_fumatore_rice][0]"]', safe_get(el, 'bio', 'Fumatore/rice', default=None))
        formInput('//input[@name="drts[field_bere][0]"]', safe_get(el, 'bio', 'Bere', default=None))
        formInput('//input[@name="drts[field_disponibile_per][0]"]', safe_get(el, 'bio', 'Disponibile per', default=None))
        formInput('//input[@name="drts[field_incontrare][0]"]', safe_get(el, 'bio', 'Incontrare', default=None))
        formInput('//input[@name="drts[field_dove_vivi][0]"]', safe_get(el, 'bio', 'Dove vivi', default=None))
    
        try:
            btn = driver.find_element(By.ID, 'post-drts-post-content-0-editor-html') 
            driver.execute_script("arguments[0].scrollIntoView();", btn)
            btn.click()
            textArea = driver.find_element(By.CLASS_NAME, 'wp-editor-area') 
            textArea.send_keys(el['aboutme'])
        except:
            pass
        
        # prices section
        moneySection('30 minuti','//input[@name="drts[field_incall_30_minuti][0][value]"]','incall')
        moneySection('45 minuti','//input[@name="drts[field_incall_45_minuti][0][value]"]','incall')
        moneySection('60 minuti','//input[@name="drts[field_incall_60_minuti][0][value]"]','incall')
        moneySection('90 minuti','//input[@name="drts[field_incall_60_minuti][0][value]"]','incall')
        moneySection(' ora cena','//input[@name="drts[field_incall_ora_cena][0][value]"]','incall')
        moneySection(' per una notte','//input[@name="drts[field_per_una_notte][0][value]"]','incall')
        moneySection(' fine settimana','//input[@name="drts[field_fine_settimana][0][value]"]','incall')
        moneySection(' ora addizionale','//input[@name="drts[field_ora_addizionale][0][value]"]','incall')
        moneySection('1 ore','//input[@name="drts[field_incall_1_ore][0][value]"]','incall')
        moneySection('2 ore','//input[@name="drts[field_incall_2_ore][0][value]"]','incall')
        moneySection('3 ore','//input[@name="drts[field_incall_3_ore][0][value]"]','incall')
        moneySection('4 ore','//input[@name="drts[field_incall_4_ore][0][value]"]','incall')
        moneySection('5 ore','//input[@name="drts[field_incall_5_ore][0][value]"]','incall')
    
        moneySection('30 minuti','//input[@name="drts[field_outcall_30_minuti][0][value]"]','outcall')
        moneySection('45 minuti','//input[@name="drts[field_outcall_45_minuti][0][value]"]','outcall')
        moneySection('60 minuti','//input[@name="drts[field_outcall_60_minuti][0][value]"]','outcall')
        moneySection('90 minuti','//input[@name="drts[field_outcall_60_minuti][0][value]"]','outcall')
        moneySection(' ora cena','//input[@name="drts[field_outcall_ora_cena][0][value]"]','outcall')
        moneySection(' per una notte','//input[@name="drts[field_outcall_per_una_notte][0][value]"]','outcall')
        moneySection(' fine settimana','//input[@name="drts[field_outcall_fine_settimana][0][value]"]','outcall')
        moneySection(' ora addizionale','//input[@name="drts[field_outcall_ora_addizionale][0][value]"]','outcall')
        moneySection('1 ore','//input[@name="drts[field_outcall_1_ore][0][value]"]','outcall')
        moneySection('2 ore','//input[@name="drts[field_outcall_2_ore][0][value]"]','outcall')
        moneySection('3 ore','//input[@name="drts[field_outcall_3_ore][0][value]"]','outcall')
        moneySection('4 ore','//input[@name="drts[field_outcall_4_ore][0][value]"]','outcall')
        moneySection('5 ore','//input[@name="drts[field_outcall_5_ore][0][value]"]','outcall')
    
    
    
        # City tour
        formInput('//input[@name="drts[field_city][0]"]', safe_get(el, 'cityTour', 'city', default=None))
        formInput('//input[@name="drts[field_data][0]"]', safe_get(el, 'cityTour', 'Data', default=None))
        formInput('//input[@name="drts[field_telefono_del_tour][0]"]', safe_get(el, 'cityTour', 'Telefono del tour', default=None))
        formInput('//input[@name="drts[field_stato][0]"]', safe_get(el, 'cityTour', 'stato', default=None))
        # City tour
    
        # Contacs section
        formInput('//input[@name="drts[field_citta_base][0]"]', safe_get(el, 'contacts', 'Città base', default=None))
        formInput('//input[@name="drts[field_phone][0]"]', safe_get(el, 'contacts', 'Telefono', default=None))
        formInput('//input[@name="drts[field_apps_available][0]"]', safe_get(el, 'contacts', 'Apps Available', default=None))
        formInput('//input[@name="drts[field_zone_citta][0]"]', safe_get(el, 'contacts', 'Zone città', default=None))
        formInput('//input[@name="drts[field_website][0]"]', safe_get(el, 'contacts', 'Web', default=None))
        formInput('//input[@name="drts[field_istruzioni_telefono][0]"]', safe_get(el, 'contacts', 'Istruzioni telefono', default=None))
        # Contacs section
        formInput('//input[@name="drts[field_foreign_id][0]"]', el['id'])
    
        formInput('//input[@name="drts[location_address][0][location][address][address]"]', safe_get(el, 'contacts', 'Città base', default=None))
        try:
            search = driver.find_element(By.CLASS_NAME, 'fa-search')
            search.click()
        except:
            pass
        
        i = 0
        j = 0
        arrayDays = [
            ['Lunedì','Monday'],
            ['Martedi', 'Tuesday'],
            ['Mercoledì', 'Wednesday'],
            ['Giovedi', 'Thursday'],
            ['Venerdi','Friday'],
            ['Sabato','Saturday'],
            ['Domenica','Sunday']
        ]
        while j < 7:
            i += selectDay(arrayDays[j][0],arrayDays[j][1],el,i)
            j += 1
        
        try:
            forClick = driver.find_element(By.XPATH, '//select[@name="drts[field_opening_hours][0][day]"]')   
            driver.execute_script("arguments[0].scrollIntoView();", forClick)
            forClick.click()
        except:
            pass
        
        if "Etnia" in el['bio']:
            category("Etnia")
            category(el['bio']['Etnia'])
        if "Nazionalità" in el['bio']:
            category("Nazionalità")
            category(el['bio']['Nazionalità'])
        try:
            publish = driver.find_element(By.ID, 'publish')
            driver.execute_script("arguments[0].scrollIntoView();", publish)
            publish.click()
        except:
            btn = driver.find_element(By.CLASS_NAME, 'swal2-close')
            btn.click() 
            publish = driver.find_element(By.ID, 'publish')
            driver.execute_script("arguments[0].scrollIntoView();", publish)
            publish.click()

driver.quit()


load_dotenv()

chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-features=NetworkService")
chrome_options.add_argument("--headless")
service = Service(executable_path=os.getenv("EXECUTABLE_PATH"))

driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get('https://e-scort.it/wp-admin/post-new.php?post_type=escorts_dir_ltg')

with open('./oldData.json','r',encoding='utf-8') as file:
    variable = json.load(file)

# login section
wait = WebDriverWait(driver, 15)  
wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="login[username]"]')))
login = driver.find_element(By.XPATH, '//input[@name="login[username]"]')
login.send_keys(os.getenv("WORDPRESS_LOGIN"))
password = driver.find_element(By.XPATH, '//input[@name="login[password]"]')
password.send_keys(os.getenv("WORDPRESS_PASSWORD"))
btn = driver.find_element(By.XPATH, '//button[@name="login[login][submit]"]') 
btn.click()
# login section
# fill Form

time.sleep(2)

def getInputVal(input):
      input_element = driver.find_element(By.XPATH, input)
      driver.execute_script("arguments[0].scrollIntoView();", input_element)
      input_value = input_element.get_attribute("value")
      return input_value

def changeVal(newVal,element):
      input_element = driver.find_element(By.XPATH, element)
      driver.execute_script("arguments[0].scrollIntoView();", input_element)
      input_element.clear()
      input_element.send_keys(newVal)

def update():
      try:
        elem = driver.find_element(By.ID,'publish')
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        elem.click()
      except:
        print('sdadas')
        pass

for el in variable:
        try:
            driver.get('https://e-scort.it/wp-admin/post.php?post=' + str(el['localId']) +'&action=edit')
            wait = WebDriverWait(driver, 15)  
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="post_title"]')))
            tourCurrent = getInputVal('//input[@name="drts[field_telefono_del_tour][0]"]')
            statoCurrent = getInputVal('//input[@name="drts[field_stato][0]"]')
            cityCurrent = getInputVal('//input[@name="drts[field_city][0]"]')
            dataCurrent = getInputVal('//input[@name="drts[field_data][0]"]')

            data = el['cityTour'].get('Data', '')
            telefone = el['cityTour'].get('Telefono del tour', '')
            stato = el['cityTour'].get('stato', '')
            city = el['cityTour'].get('city', '')
            isUpdate = False
            if city != cityCurrent:
                  changeVal(city,'//input[@name="drts[field_telefono_del_tour][0]"]')
                  isUpdate = True
            if telefone != tourCurrent:
                  telefone(city,'//input[@name="drts[field_city][0]"]')
                  isUpdate = True
            if statoCurrent != stato:
                  changeVal(stato,'//input[@name="drts[field_stato][0]"]')
                  isUpdate = True
            if dataCurrent != data:
                  changeVal(data,'//input[@name="drts[field_data][0]"]')
                  isUpdate = True
            if isUpdate == True:
                print(el['localId'])
                update()
        except:
             continue
        
driver.quit()
