from app.config import url_scraper, array_search
from app.utils.utils import Utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from app.application.services.fetch_service import FetchServices
from app.infraestructura.repositories.data_repository import DataRepository
from app.infraestructura.drivers.selenium_driver import SeleniumDriver
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep


class ScraperService:
    def __init__(self):
        self.arr_process_search = array_search
        self.current_page = 1
        self.pagination = 0
        self.fetch_services = FetchServices()
        self.data_repository = DataRepository()

    def fetch_all_act_jud(self, list_process, process_id):
        """
        Fetches all judicial acts details for a given process and process ID.

        Args:
            list_process (list): A list of processes.
            process_id (str): The ID of the process to fetch details for.

        Returns:
            list: A list of processes with updated subprocess details.

        Description:
            This function fetches the details of judicial acts for each subprocess in the given process. It uses the `Utils.extract_info_subprocess` function to extract the necessary information from the subprocesses. It then uses a `ThreadPoolExecutor` to fetch the details in parallel. The results are combined into a single dictionary and then updated in the original list of processes. Finally, the updated list of processes is returned.

        Note:
            This function assumes that the `Utils.extract_info_subprocess` function is defined in the `Utils` class.
        """
        extract_subprocess = Utils.extract_info_sub_process(
            list_process[process_id])

        combined_results = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(
                self.fetch_services.fetch_actuaciones_judiciales, extract_subprocess))
            for result in results:
                combined_results.update(result)

        for process in list_process[process_id]:
            for subprocess in process['details']['subProcess']:
                id_judicatura = subprocess["idJudicatura"]
                if id_judicatura in combined_results:
                    subprocess["actuacionesJudiciales"] = combined_results[id_judicatura]

        return list_process

    def fetch_all_cases(self, list_process, process_id):
        """
        Fetches the details of multiple cases in parallel.

        Args:
            list_process (dict): A dictionary containing the list of processes.
            process_id (str): The ID of the process to fetch details for.

        Returns:
            dict: A dictionary containing the updated list of processes.

        Description:
            This function fetches the details of multiple cases in parallel using a ThreadPoolExecutor. It takes a list of processes and a process ID as input. It extracts the case IDs from the list of processes and uses the ThreadPoolExecutor to fetch the details of each case in parallel. The results are then combined into a single list and updated in the original list of processes. Finally, the updated list of processes is returned.
        """

        case_ids = [case['idJuicio']
                    for case in list_process[process_id]]
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(
                self.fetch_services.fetch_case_details, case_ids))

        for i in range(len(list_process[process_id])):
            list_process[process_id][i]['details'].update(results[i])

        return list_process

    def get_pagination(self, wait):
        """
        Retrieves the pagination information from the web page.

        Args:
            wait (WebDriverWait): The WebDriverWait object used to wait for elements to be present.

        Returns:
            int or Exception: The number of pages if pagination is available, 0 if there are no results, or an Exception if an error occurs.

        Description:
            This function waits for the presence of the element with the CSS selector ".cantidadMovimiento" and retrieves the text of that element. If the text is not empty, it splits the text by ': ' to extract the number of results. If the number of results is greater than 0, it waits for the presence of all elements with the CSS selector ".mat-mdc-paginator-range-label" and retrieves the text of the first element. It then splits the text by ' de ' to extract the number of pages. Finally, it returns the number of pages. If there are no results or an error occurs, it returns 0 or the Exception object respectively.
        """
        try:
            sleep(3)
            resultados_element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".cantidadMovimiento")
                )
            )

            if resultados_element:
                resultados_text = int(
                    resultados_element.text.split(': ')[1])
                if resultados_text > 0:
                    pagination = wait.until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, ".mat-mdc-paginator-range-label")
                        )
                    )
                    return int(pagination[0].text.split(' de ')[1])
                else:
                    return 0
        except Exception as e:
            return e

    def reload_get_pagination(self, wait, data):
        """
        Reloads the pagination information by clicking on a link and navigating back.

        Args:
            wait (WebDriverWait): The WebDriverWait object used to wait for elements to be present.
            data (list): A list of elements containing the first juicio ID.

        Description:
            This function retrieves the first juicio ID from the first element in the data list. It then waits for the presence of an element with the CSS selector 'a[aria-label="Vínculo para ingresar a los movimientos del proceso {id_first_juicio}"]' and clicks on it. After a 4-second delay, it waits for the presence of an element with the CSS selector '.btn-regresar' and clicks on it.
        """
        id_first_juicio = data[0].find_element(
            By.CSS_SELECTOR, ".numero-proceso").text

        elemento_href = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 f'a[aria-label="Vínculo para ingresar a los movimientos del proceso {id_first_juicio}"]')
            ))

        elemento_href.click()
        sleep(4)
        btn_back = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.btn-regresar')))
        btn_back.click()

    def wait_for_page_data_load(self, wait):
        """
        Waits for all elements with the CSS selector ".causa-individual" to be present on the page.

        Args:
            wait (WebDriverWait): The WebDriverWait object used to wait for elements to be present.

        Returns:
            list: A list of WebElement objects representing the elements with the CSS selector ".causa-individual".

        Description:
            This function uses the WebDriverWait object to wait for all elements with the CSS selector ".causa-individual" to be present on the page. It waits for the presence of all elements with the specified CSS selector and returns a list of WebElement objects representing those elements.
        """
        causas_individuales = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".causa-individual")
            )
        )

        return causas_individuales

    def search_data(self, wait, process_type, process_id):
        """
        Searches for data based on the given process type and process ID.

        Args:
            wait (WebDriverWait): The WebDriverWait object used to wait for elements to be present.
            process_type (str): The type of the process. Can be either "ofendido" or "demandado/procesado".
            process_id (str): The ID of the process to search for.

        Returns:
            dict or int: If the data is found, returns the pagination information. If an error occurs, returns a dictionary with the error message.

        Description:
            This function searches for data based on the given process type and process ID. It uses the WebDriverWait object to wait for the input element with the specified placeholder to be present on the page. It then enters the process ID into the input element and presses the Enter key. After a short delay, it calls the `get_pagination` method to retrieve the pagination information.

            If an error occurs during the search process, a dictionary with the error message is returned.
        """
        try:
            if process_type == "ofendido":
                placeholder = 'Ingrese la identificación del Actor/Ofendido'
            else:
                placeholder = 'Ingrese la identificación del Demandado/Procesado'

            input_element = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"input[placeholder='{placeholder}']")
            ))

            input_element.send_keys(process_id)
            input_element.send_keys(Keys.ENTER)
            sleep(1)
            return self.get_pagination(wait)
        except Exception as e:
            return {'error': str(e)}

    def next_page(self, wait):
        """
        Clicks on the next page button on a web page.

        Args:
            wait (WebDriverWait): The WebDriverWait object used to wait for elements to be present.

        Returns:
            Exception or None: If an exception occurs during the process, it is returned. Otherwise, None is returned.

        Description:
            This function uses the WebDriverWait object to wait for the presence of the next page button on a web page. Once the button is located, it is clicked. If an exception occurs during the process, it is returned. Otherwise, None is returned.
        """
        try:
            next_page = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".mat-mdc-tooltip-trigger.mat-mdc-paginator-navigation-next.mdc-icon-button.mat-mdc-icon-button.mat-unthemed.mat-mdc-button-base")
                )
            )
            next_page.click()
        except Exception as e:
            return e

    def scrape_process(self, process_type, process_id):
        """
        Scrapes a process based on the given process type and process ID.

        Args:
            process_type (str): The type of the process. Can be either "ofendido" or "demandado".
            process_id (str): The ID of the process to scrape.

        Returns:
            dict: A dictionary containing the process ID, process type, and status of the scraping process.
                - process_id (str): The ID of the process.
                - process_type (str): The type of the process.
                - status (str): The status of the scraping process. Can be either "success" or "error".
                - error (str, optional): The error message if the scraping process encounters an exception.

        Description:
            This function uses Selenium to scrape a process based on the given process type and process ID.
            It initializes a Selenium driver and a WebDriverWait object.
            It navigates to the URL scraper and searches for data based on the process type and process ID.
            If no pagination are found, it reloads the page and gets the pagination information.
            It then iterates through each page and fetches the necessary data.
            The fetched data is updated in the data repository.
            The function returns a dictionary containing the process ID, process type, and status of the scraping process.
            If an exception occurs during the scraping process, the function returns a dictionary with the error message.
        """
        driver = SeleniumDriver.get_driver()
        wait = WebDriverWait(driver, 50)

        try:
            driver.get(url_scraper)
            pages = self.search_data(wait, process_type, process_id)
            current_page = 1

            if pages == 0:
                list_data = self.wait_for_page_data_load(wait)
                self.reload_get_pagination(wait, list_data)
                pages = self.get_pagination(wait)

            while current_page <= pages:
                if (current_page > 1):
                    self.next_page(wait)

                list_process = self.wait_for_page_data_load(wait)
                format_list_causas = Utils.format_init(
                    list_process, process_id, process_type)

                result_details = self.fetch_all_cases(
                    format_list_causas, process_id)

                result_act_jud = self.fetch_all_act_jud(
                    result_details, process_id)

                sleep(3)
                self.data_repository.update_data(result_act_jud, process_id)
                sleep(1)
                current_page += 1
            driver.quit()
            return {'process_id': process_id, 'process_type': process_type, 'status': 'success'}

        except Exception as e:
            return {'process_id': process_id, 'process_type': process_type, 'status': 'error', 'error': str(e)}

    def init_scraper(self):
        """
        Executes the scraping process concurrently using a ThreadPoolExecutor.

        Performs up to 15 queries in parallel and handles any potential errors that may occur during the process.

        Returns:
            JSON with the completion message of the process or a dictionary with the error.
        """
        try:
            self.data_repository.reset_data()
            results = []
            with ThreadPoolExecutor(max_workers=15) as executor:
                futures = {
                    executor.submit(self.scrape_process, item['type'], item['id']): item['id']
                    for item in self.arr_process_search
                }
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        results.append(
                            {id: result['process_id'], type: result['process_type']})
                    except Exception as e:
                        results.append(
                            {'process_id': futures[future], 'status': 'error', 'error': str(e)})

            return {'msg': 'The scraping process has been completed'}, 200
        except Exception as e:
            return {'error': str(e)}
