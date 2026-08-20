# CHANGES — ветка `anthropic-claude-opus-5-default`

Агент: `anthropic/claude-opus-5@default`. Оригинальный
`benchmark_task_github_skill.ipynb` **не изменён**.

## Добавленные файлы

| Файл | Что это |
|---|---|
| `CAPABILITIES_anthropic-claude-opus-5-default.md` | Моя роль, что я умею менять, чего мне не хватает и какие инструменты предлагаю добавить. |
| `benchmark_task_github_skill_v2.ipynb` | Рабочая v2 бенчмарка с расширенным тулингом и issue-driven задачей. |
| `CHANGES_anthropic-claude-opus-5-default.md` | Этот файл. |

## Что нового в v2 (кратко)

**Транспорт.** `_gh_request` с ретраями (5xx, вторичный rate limit),
`_gh_paginate` для списочных эндпоинтов, `_clip` обрезает вывод инструмента до
12 000 символов, чтобы один `read_file` не съедал контекст.

**Было 4 инструмента → стало 15:**

* Навигация: `list_files` (рекурсивный tree), `search_code` (grep по ветке),
  `read_file(from_my_branch, start_line, max_lines)` — чтение из своей ветки и
  по диапазону строк.
* Запись: `patch_file` (замена подстроки вместо перезаписи целого файла),
  `delete_file`, `write_file(commit_message)`, `diff_vs_base`.
* Issues: `list_issues` (все, open+closed, PR отфильтрованы), `get_issue`
  (тело + все комментарии), `comment_issue`, `report_work`, `open_pull_request`.
* Ветки: `create_issue_branch(N)` → `<slug>/issue-<N>`, становится текущей
  рабочей веткой агента.

**Безопасность.** Имя ветки по-прежнему не приходит от модели: оно строится из
slug и номера issue. Функция `_guard` дополнительно запрещает любую запись в
ветку без префикса slug — `main` и чужие ветки защищены.

**Новая задача `github_issue_resolution`.** Проверка успеха машинная и
двойная: ветка `<slug>/issue-<N>` должна опережать `main` минимум на 1 коммит
**и** в issue должен быть комментарий, содержащий имя этой ветки. `report_work`
формирует такой комментарий автоматически: ссылка на ветку, ссылка на
`compare/main...<branch>`, число коммитов, список изменённых файлов, резюме.

**Смоук-тест** `smoke_test()` — раздел 7: проверяет ветки, дерево файлов,
issues и compare без единого вызова LLM. Если issues отдают 403 — у токена нет
нужного scope, и это видно до траты бюджета.

## Что требуется от владельца репозитория

Расширить fine-grained PAT: **`Issues: Read and write`** (обязательно для
пункта про комментарии), `Pull requests: Read and write` (опционально),
`Contents: RW` и `Metadata: R` уже есть.

## Не сделано / следующий шаг

* Не выполнено ни одной ячейки — у меня нет исполнения кода, только запись файлов.
* `search_code` читает файлы по одному; на большом репозитории лучше перейти на
  GitHub Search API с fallback на текущую реализацию.
* Нет автоматического разрешения конфликтов при `patch_file`, если ветка отстала
  от `main` — стоит добавить `behind_by` warning в `diff_vs_base`.
