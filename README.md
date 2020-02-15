# LimeSurvey Factorial Vignette Survey
This framework is building on the great work by Lindsay Stevens (https://github.com/lindsay-stevens/limesurveyrc2api)

I required a survey platform to host a factorial vignette survey with full flexibility of factors across vignettes. Additionally, I required information being 'piped' from answers of questions to the following. After discovering LimeSurvey and it's API, I used jinja2 in Python to generate the survey. LimeSurvey offered additional flexibility by allowing the use of JavaScript. Some additional scripts and routines for deployment were added later.

The templates support the following question types on LimeSurvey
- array
- array (texts)
- List (dropdown) 
- List (radio) 
- Ranking 
