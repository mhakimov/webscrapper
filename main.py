from webofscience.webofscience import Webofscience

with Webofscience() as bot:
    bot.land_libguides_page()
    bot.navigate_to_webofscience()
    bot.search_for_theme("Electric vehicle")
    bot.apply_filtering()
    bot.collect_authors_info()






