# Ali-Acronym

An Acronym Explainer bot

Initially created following this guide: https://python.plainenglish.io/lets-create-a-slackbot-cause-why-not-2972474bf5c1

This bot allows 3 types of interaction (see script). Currently, it uses a dictionary 
as a database, and only allows read interactions

This is built entirely with Python

# Currently

So been exploring various options, and looks like Zappa is the best bet to get this thing spun up on cloud
quickly and repeatably. Try tomorrow. If that doesn't work, I'm gonna write a goddam bash command to zip this,
thing and have that for repeatability

## Script

/ali_explain
- If it recognises 1 acronym and has 1 definition in the database (ex: MOD)
  - "I recognise MOD as {meaning}. {description}. And it belong to the {department}"
- If it recognises 1 acronym and has multiple definitions in the database (ex: AE)
  - "I recognise AE as having multiple meanings. They are:
    - {meaning}. {description}. And it belongs to the {department}"
    - Repeat list til meaning done
- If it gets sent multiple acronyms it sends each script as a separate message
- If it gets sent "help":
  - It sends back a help message

IM:
Acts like ali_explain command but with some extra easter eggs

@Ali_Acronym
- "Here are the acronyms I've found, {acronyms}"
- And then explains them in individual order
    

## Database structure

You can refer to `acronym_database/acronym_data_struct.py` but it's a key:value store,
which contains either 

```json
{
  "Acronym": {
    "meaning": "Full Name",
    "description": "Extra details about what the acronym means",
    "department": "Government department if relevant"
  }
}
```

For example:
```json
{
  "MOD": {
    "meaning": "Ministry of Defence",
    "description": "",
    "department": "MoD"
  }
}
```

or a structure of multiple acronyms

```json
{
  "Acronym": {
    "Acronym (category_1)": {
      "meaning": "Full Name",
      "description": "Extra details about what the acronym means",
      "department": "Government department if relevant"
    },
    "Acronym (category_2)": {
      "meaning": "Full Name",
      "description": "Extra details about what the acronym means",
      "department": "Government department if relevant"
    }
  }
}
```

For example:

```json
{
  "YCS": {
    "YCS": {
      "meaning": "Youth Cohort Study",
      "description": "A series of longitudinal surveys that contacts a sample of an academic year-group or \"cohort\" of young people in the spring following completion of education and usually annually until they are aged 19 or 20. The survey looks at young people's education and labour market experience, their training and qualifications and a wide range of other issues, including socio-demographic variables.Source: DfE RS Gateway as at 2011-01-17",
      "department": "DfE"
    },
    "YCS (service)": {
      "meaning": "Youth Custody Service",
      "description": "https://www.gov.uk/government/organisations/youth-custody-service",
      "department": "MoJ"
    }
  }
}
```