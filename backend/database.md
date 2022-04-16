# Database

Game IDs are numbers

Circuit ID are letters

Team IDs are made of letters + numbers

All of them are string values.

## User


| Key         | Definition | Description      |
| ----------- | ---------- | ---------------- |
| id          | str        | User ID          |
| name        | str        | User name        |
| email       | str        | User email       |
| permissions | list       | User permissions |


## Game

| Key     | Type | Description                      |
| ------- | ---- | -------------------------------- |
| id      | str  | Game ID (1, 2, 3, ...)           |
| hash    | str  | Game hash id (to avoid cheating) |
| circuit | str  | Circuit ID (max 2 letters)       |
| name    | str  | Game name                        |
| leaders | list | Game leaders                     |
| matches | list | Ordered list of match ids        |
| weight  | int  | Points received by the winner    |

## Team

| Key          | Definition | Description                                                  |
| ------------ | ---------- | ------------------------------------------------------------ |
| id           | str        | Team ID (A1, A2, B1, ...)                                    |
| number       | int        | Number used to randomly distribute the teams across the games \* |
| section      | str        | Section name                                                 |
| category     | str        | (Loups, Lutins, Balas)                                       |
| hash         | str        | Team hash id (to avoid cheating)                             |
| matches      | list       | Ordered list of match ids                                    |
| ignore_score | bool       | Do not count this team in the section mean score             |

\* do **not** edit manually

## Match

| Key            | Definition | Description                       |
|----------------| ---------- | --------------------------------- |
| id             | str        | Unique id                         |
| game_id        | str        | Game ID                           |
| time           | int        | Index in the schedule             |
| start_time     | str        | Start time (e.g. "10h00")         |
| stop_time      | str        | Stop time (e.g. "10h15")          |
| player_ids     | list       | Players codes                     |
| player_numbers | list       | Players number (not id)           |
| winner         | str        | Winner code                       |
| loser          | str        | Loser code                        |
| draw           | bool       | True if evenly won                |
| reporter       | str        | Name of the reporter of the score |

## Settings

| Key  | Type | Description |
| ---- | ---- | ----------- |
|      |      |             |
|      |      |             |
|      |      |             |

