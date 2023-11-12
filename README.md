<br />

<p align="middle">
    <img src="https://github.com/antz22/edulecture.ai/blob/main/imgs/hero.png" width="100%" style="margin:0; padding: 0">
</p>

<br />

<p align="middle">
    EduLecture.ai is a groundbreaking voice-generative AI tool that uses machine learning to bridge the gaps in accessibility and quality of remote education.
</p>

# Inspiration
All students have been in a situation where they’re reviewing lecture slides and simply cannot follow along. Grasping lecture material, particularly for lessons loaded with abstract visual models, can be difficult without an auditory aid. That’s why EduLecture.ai is here to help. By increasing the accessibility of remote education, EduLecture.ai boosts student comprehension and engagement. Students remain more engaged when hearing a lecture in a familiar teacher’s voice, resulting in improved academic performance.

# What it does
EduLecture.ai is a website that allows educators to seamlessly generate a video presentation of their lecture. Using AI and machine learning, EduLecture.ai accepts a short audio sample of the educator’s voice and their Google Slides lecture, accompanied by slide notes, to create a video lecture narrated in the educator’s unique voice. These videos are then uploaded and saved to the educator’s online profile, on which students can easily access their educator's content, whether it's for supplementary review material, makeup work, or much more.

# How we built it
EduLecture.ai was built using a combination of React, Django, and Python. In order to build the frontend for EduLecture.ai, we used React.js to easily integrate interactions with the API. For the backend, we coded a server using Django Rest Framework for the API endpoints that the frontend called. On the backend, we used different Python libraries for the voice-generative AI tooling that lived in the Django server.

# Challenges we ran into
Some of the major challenges we ran into included issues with authenticating the Google Cloud Platform Project, as well as creating an authentication system between Django and React. It was our first time using Django and React together, so there was quite a bit to learn there. We also ran into additional issues with managing files on the Django server for generating the AI-narrated video.

# Accomplishments that we're proud of
We’re proud of the quick timing it takes to process the input lecture and convert it into a functional, professional video. We’re also proud of the concept and potential of our idea, as it’s a novel application of cutting-edge AI technology that truly addresses issues of accessibility for students and teachers alike.

# What we learned
We learned how to create a website using React and Django together. We also learned how to set up a Google Cloud and work with Google APIs and authentication. Finally, we learned how to integrate AI tools into the full-stack framework development pipeline.

# What's next for EduLecture.ai
We aim to expand our features and implement a premium plan for users. Educators without the premium plan will still be able to access our basic functionalities. In addition, subscribers to the premium plan will have more advanced features such as translation, collaboration with other users, auto-generation of thorough lecture notes from sparse bulleted notes, and more.

# Built With

```
django
django-rest-framework
djoser
elevenlabs
google
google-cloud
html
css
machine-learning
opencv
python
react
```