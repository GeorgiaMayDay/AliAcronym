# Slack Bot template

This is my slack bot template 

Initially created following this guide: https://python.plainenglish.io/lets-create-a-slackbot-cause-why-not-2972474bf5c1

Hopefully going to turn into an acroymn explainer bot

# WIP: Currently

I need to add some kind of nested structure to allow for the same acronym having multiple meanings

So the current thinking for this is:

Okay made a reasonable database

Now need to figure out to present/how to word the commands

Current thoughts:

/ali_explain takes one or a list of acronyms and returns what they could/do mean

meantion is used in a thread to collect the parent message so you can break down the acronym in it
Outside of a thread it delivers a help message explaining how it used, and what /ali_explain does



Will probably also want to add a jargon command

# Database structure

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