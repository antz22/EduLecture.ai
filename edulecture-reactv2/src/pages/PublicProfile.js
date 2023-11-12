import React, { useEffect, useState } from "react";
import AnimationRevealPage from "helpers/AnimationRevealPage.js";
import { Container, ContentWithPaddingXl } from "components/misc/Layouts";
import tw from "twin.macro";
import styled from "styled-components";
import { css } from "styled-components/macro";
import Header from "components/headers/light.js";
import Footer from "components/footers/FiveColumnWithInputForm.js";
import { SectionHeading } from "components/misc/Headings";
import { PrimaryButton } from "components/misc/Buttons";
import axios from "axios";

import Art from "../assets/art.png";
import Bio from "../assets/biology.jpeg";
import Business from "../assets/business.jpeg";
import Chem from "../assets/chemistry.jpeg";
import English from "../assets/english.jpeg";
import ForeignLanguage from "../assets/foreign-language.jpeg";
import History from "../assets/history.jpeg";
import Math from "../assets/math.jpeg";
import Physics from "../assets/physics.jpeg";
import { useParams } from "react-router-dom";

const HeadingRow = tw.div`flex`;
const Heading = tw(SectionHeading)`text-gray-900`;
const Posts = tw.div`mt-6 sm:-mr-8 flex flex-wrap`;
const PostContainer = styled.div`
  ${tw`mt-10 w-full sm:w-1/2 lg:w-1/3 sm:pr-8`}
  ${props =>
    props.featured &&
    css`
      ${tw`w-full!`}
      ${Post} {
        ${tw`sm:flex-row! h-full sm:pr-4`}
      }
      ${Image} {
        ${tw`sm:h-96 sm:min-h-full sm:w-1/2 lg:w-2/3 sm:rounded-t-none sm:rounded-l-lg`}
      }
      ${Info} {
        ${tw`sm:-mr-4 sm:pl-8 sm:flex-1 sm:rounded-none sm:rounded-r-lg sm:border-t-2 sm:border-l-0`}
      }
      ${Description} {
        ${tw`text-sm mt-3 leading-loose text-gray-600 font-medium`}
      }
    `}
`;
const Post = tw.div`cursor-pointer flex flex-col bg-gray-100 rounded-lg`;
const Image = styled.div`
  ${props => css`background-image: url("${props.imageSrc}");`}
  ${tw`h-64 w-full bg-cover bg-center rounded-t-lg`}
`;
const Info = tw.div`p-8 border-2 border-t-0 rounded-lg rounded-t-none`;
const Category = tw.div`uppercase text-primary-500 text-xs font-bold tracking-widest leading-loose after:content after:block after:border-b-2 after:border-primary-500 after:w-8`;
const CreationDate = tw.div`mt-4 uppercase text-gray-600 italic font-semibold text-xs`;
const Title = tw.div`mt-1 font-black text-2xl text-gray-900 group-hover:text-primary-500 transition duration-300`;
const Description = tw.div``;

const ButtonContainer = tw.div`flex justify-center`;
const LoadMoreButton = tw(PrimaryButton)`mt-16 mx-auto`;

export default ({
  headingText = "Lectures",
}) => {

  const [visible, setVisible] = useState(7);
  const [lectures, setLectures] = useState([]);
  const [name, setName] = useState('');
  const { userName } = useParams();
  const client = axios.create({
    baseURL: "http://127.0.0.1:8000"
  });

  const subjectImages = {
    "Chemistry": Chem,
    "Biology": Bio,
    "Physics": Physics,
    "English": English,
    "History": History,
    "Math": Math,
    "Art": Art,
    "Business": Business,
    "Foreign Language": ForeignLanguage,
  }

  const onLoadMoreClick = () => {
    setVisible(v => v + 6);
  };

  useEffect(() => {
    const body = {
        "user_name": userName,
    };
    client.post("/api/v1/get-user-lectures/", body, {
      headers: {
        "Authorization": "Token " + localStorage.getItem("token"),
      }
    }).then(res => {
      setLectures(res.data);
      setName(res.data[0]["user_name"]);
      console.log(res.data);
    }).catch(err => {
      console.log(err);
    });
  }, [])

  return (
    <AnimationRevealPage>
      <Header />
      <Container>
        <ContentWithPaddingXl>
          <HeadingRow>
            <Heading>{name}'s Lectures</Heading>
          </HeadingRow>
          <Posts>
            {lectures.slice(0, visible).map((lecture, index) => (
              <PostContainer key={index} featured={false}>
                <Post className="group" as="a" href={lecture.image_link}>
                  <iframe src={lecture.video_link} width="405" height="270" allow="autoplay"></iframe>
                  <Info>
                    <Category>{lecture.subject_name}</Category>
                    <CreationDate>{lecture.user_name}</CreationDate>
                    <Title>{lecture.title}</Title>
                    <Description>{lecture.description}</Description>
                  </Info>
                </Post>
              </PostContainer>
            ))}
          </Posts>
          {visible < lectures.length && (
            <ButtonContainer>
              <LoadMoreButton onClick={onLoadMoreClick}>Load More</LoadMoreButton>
            </ButtonContainer>
          )}
        </ContentWithPaddingXl>
      </Container>
      <Footer />
    </AnimationRevealPage>
  );
};