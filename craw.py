from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


games = {}
x = 0


while True:
    if x == 0:
        game = input('Digite o jogo desejado: ')
    else:
        game = input('Digite o jogo desejado (ou aperte enter novamente para continuar): ')
    if not game:
        break
    games[game] = {}
    x += 1



chrome_options = Options()
chrome_options.headless = True
browser = webdriver.Chrome(options=chrome_options,)

browser.get('https://store.steampowered.com/')

for a_game in games:
    print('Finding info for "' + a_game + '"')

     
    
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#store_nav_search_term"))).send_keys(a_game)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#search_suggestion_contents>a"))).click()
    

    
    try:
        browser.find_element(By.CSS_SELECTOR,'.agegate_birthday_selector')
        select = Select(browser.find_element(By.ID,'ageYear'))
        select.select_by_value('2004')
        browser.find_element(By.CSS_SELECTOR,'a.btnv6_blue_hoverfade:nth-child(1)').click()
    except NoSuchElementException:
        pass

    
    
    games[a_game]['name'] = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.apphub_AppName'))).text

    
    
    mac = False
    linux = False
    try:
        browser.find_element(By.CSS_SELECTOR,'div.game_area_purchase_game_wrapper:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                             'span:nth-child(2)')
        mac = True
    except NoSuchElementException:
        pass

    try:
        browser.find_element(By.CSS_SELECTOR,'div.game_area_purchase_game_wrapper:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                             'span:nth-child(3)')
        linux = True
    except NoSuchElementException:
        pass

    if mac and linux:
        games[a_game]['platform'] = 'all'
    elif mac:
        games[a_game]['platform'] = 'mac'
    elif linux:
        games[a_game]['platform'] = 'linux'
    else:
        games[a_game]['platform'] = 'windows'

    
    
    discounted = False
    try:
        games[a_game]['price'] = browser.find_element(By.CSS_SELECTOR,'div.game_purchase_action:nth-child(4) > div:nth-child(1) > div:nth-child(1)').text
    except NoSuchElementException:
        try:
            games[a_game]['before_price'] = browser.find_element(By.CLASS_NAME,'discount_original_price').text
            games[a_game]['after_price'] = browser.find_element(By.CLASS_NAME,'discount_final_price').text
        except NoSuchElementException:
            try:
                games[a_game]['price'] = 'FREE'
            except NoSuchElementException:
                games[a_game]['bundle_price'] = browser.find_element(By.CSS_SELECTOR,'div.game_purchase_action_bg:nth-child(2) > div:nth-child(1)')
    except Exception:
        games[a_game]['price'] = 'Error: Unable to get price'

    
    
    games[a_game]['specs'] = browser.find_element(By.CSS_SELECTOR,'.game_area_sys_req').text


print('Dados coletados, Fechando navegador \n')
print('********************************************')
browser.close()

for each_game in games.keys():
    print('GAME: ' + games[each_game]['name'].upper())

    
    if games[each_game]['platform'] == 'all':
        print('Plataformas compativeis: Windows, Mac and Linux')
    elif games[each_game]['platform'] == 'mac':
        print('Plataformas compativeis: Windows and Mac')
    elif games[each_game]['platform'] == 'linux':
        print('Plataformas compativeis: Windows and Linux')
    else:
        print('Plataforma compativel: Apenas Windows')
    print('\n')

    
    try:
        print('Price: Discounted ' + games[each_game]['after_price'] + ' from ' + games[each_game]['before_price'])
    except KeyError:
        print('Price: ' + games[each_game]['price'])
    except Exception:
        print('Bundled Price: ' + games[each_game]['bundle_price'])
    print('\n')

    
    print('Seu sistema precisará de: \n')
    print('-------------------------------- \n')
    print(games[each_game]['specs'])
    print('--------------------------------')
    input('Pressione Enter para continuar: ')

print('Finalizado com sucesso')
