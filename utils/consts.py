# Global constants

## config file name
CONFIG_FILE_NAME = 'config.ini'

## Statistics table entry unique ID
STATISTICS_UNIQUE_ID = 1

## time format 24-hour to 12-hour mapper
TF_24TO12 = ['12pm', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am',
             '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm']

## Keyboards
### Yes/No keyboard and re pattern
YES_NO_KEYBOARD = [['Sí'],['No']]
YES_NO_RE_PATTERN = '^(Sí|No)$'
### Available devotionals keyboard
DEVOTIONALS_KEYBOARD = [['¡Maranata: El Señor Viene!'], ['El Conflicto de los Siglos']]
DEVOTIONALS_RE_PATTERN = '^(¡Maranata: El Señor Viene!|El Conflicto de los Siglos)$'
### Pick up hours for sending devotional
HOUR_KEYBOARD = [['12pm', '1am', '2am', '3am'], ['4am', '5am', '6am', '7am'], ['8am', '9am', '10am', '11am'],
                 ['12am', '1pm', '2pm', '3pm'], ['4pm', '5pm', '6pm', '7pm'], ['8pm', '9pm', '10pm', '11pm']]
### Hours format re pattern
HOUR_RE_PATTERN = '^\d(\d)?(a|p)+m$'
### Preference pickup and change keyboards
PREFERENCE_CHANGE_KEYBOARD = [['País'], ['Hora'], ['Lectura'], ['Nada']]
CONT_PREFERENCE_CHANGE_KEYBOARD = [['País'], ['Hora'], ['Lectura'], ['Listo']]
### Preference pickup and change pattern
PREFERENCE_CHANGE_RE_PATTERN = '^(País|Hora|Lectura|Nada|Listo)$'

## Max message send retries
MAX_SEND_RETRIES = 20
## Max reachable delay in seconds between successive message resendings
MAX_RESEND_DELAY = 300

## Least necessary inter-message time interval in ms posed by the Telegram Bot API
##  see https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
LEAST_BOT_SEND_MS = 33

## Number of subscriptions appeared by row when selecting a subscription for modifications
SUBSCRIPTIONS_BY_ROW = 4

## RE to recognize a two-digit pattern for selecting subscription to modify
SUBSCRIPTION_SELECT_PATTERN = '^\d(\d)?$'