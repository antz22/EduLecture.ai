import React, {useState} from "react";
import tw from "twin.macro";
import styled from "styled-components";
import { css } from "styled-components/macro"; //eslint-disable-line
import { SectionHeading, Subheading as SubheadingBase } from "components/misc/Headings.js";
import { SectionDescription } from "components/misc/Typography.js";
import { PrimaryButton as PrimaryButtonBase } from "components/misc/Buttons.js";
import { Container, ContentWithPaddingXl } from "components/misc/Layouts.js";
import { ReactComponent as SvgDecoratorBlob1 } from "images/svg-decorator-blob-6.svg";
import { ReactComponent as SvgDecoratorBlob2 } from "images/svg-decorator-blob-7.svg";
import axios from "axios";
import useDrivePicker from "react-google-drive-picker";
import { useNavigate } from "react-router-dom";

const HeaderContainer = tw.div`w-full flex flex-col items-center`;
const Subheading = tw(SubheadingBase)`mb-4`;
const Heading = tw(SectionHeading)`w-full`;
const Description = tw(SectionDescription)`w-full text-center`;

const PlanDurationSwitcher = tw.div`block w-full max-w-xs sm:inline-block sm:w-auto border-2 rounded-full px-1 py-1 mt-8`;
const SwitchButton = styled.button`
  ${tw`w-1/2 sm:w-32 px-4 sm:px-8 py-3 rounded-full focus:outline-none text-sm font-bold text-gray-700 transition duration-300`}
  ${props => props.active && tw`bg-primary-500 text-gray-100`}
`;

const PlansContainer = tw.div`flex justify-center flex-col items-center relative mt-12`;
const Plan = styled.div`
  ${tw`w-full max-w-72 mt-16 md:mr-12 md:last:mr-0 text-center px-8 rounded-lg relative text-gray-900 bg-white flex flex-col shadow-raised`}

  ${props =>
    props.featured &&
    css`
      ${tw`border-2 border-gray-200 shadow-none`}
    `}
`;

const PlanHeader = styled.div`
  ${tw`flex flex-col leading-relaxed py-8 -mx-8 bg-gray-100 rounded-t-lg`}
  .name {
    ${tw`font-bold text-xl`}
  }
  .price {
    ${tw`font-bold text-4xl sm:text-5xl my-1`}
  }
  .slash {
    ${tw`text-xl text-gray-500`}
  }
  .duration {
    ${tw`lowercase text-gray-500 font-medium tracking-widest`}
  }
  .mainFeature {
    ${tw`text-gray-500 text-sm font-medium tracking-wide`}
  }
`;
const PlanFeatures = styled.div`
  ${tw`flex flex-col -mx-8 px-8 py-8 flex-1 text-sm`}
  .feature {
    ${tw`mt-5 first:mt-0 font-semibold text-gray-500`}
  }
`;

const PlanAction = tw.div`px-4 pb-8 mt-8`;
const BuyNowButton = styled(PrimaryButtonBase)`
  ${tw`rounded-full tracking-wider py-4 w-full text-sm hover:shadow-xl transform hocus:translate-x-px hocus:-translate-y-px focus:shadow-outline`}
`;

const DecoratorBlob1 = styled(SvgDecoratorBlob1)`
  ${tw`pointer-events-none -z-20 absolute left-0 bottom-0 h-64 w-64 opacity-25 transform -translate-x-2/3 -translate-y-1/2`}
`;
const DecoratorBlob2 = styled(SvgDecoratorBlob2)`
  ${tw`pointer-events-none -z-20 absolute right-0 top-0 h-64 w-64 opacity-25 transform translate-x-2/3 translate-y-1/2 fill-current text-teal-300`}
`;

const Input = tw.input`w-3/6 self-center px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white mt-5 first:mt-0`;
const LongInput = tw.textarea`w-3/6 self-center px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white mt-5 first:mt-0`;

export default ({
  subheading = "Upload",
  heading = "Easy Lecture Creation.",
  description = "Upload your lecture slides and notes, and we'll use AI and Machine Learning to create a video lecture using your voice, just for you.",
  plans = null,
  primaryButtonText = "Buy Now",
  planDurations = [
    {
      text: "Slides",
      switcherText: "Slides Only",
    },
    {
      text: "Notes",
      switcherText: "Slides + Notes",
    }
  ]
}) => {
  const defaultPlans = [
    {
      name: "Free Plan",
      durationPrices: ["$0", "$0"],
      mainFeature: "For Personal Blogs",
      features: ["30 Templates", "7 Landing Pages", "12 Internal Pages", "Basic Assistance"]
    },
  ];

  if (!plans) plans = defaultPlans;

  const [activeDurationIndex, setActiveDurationIndex] = useState(0);

  const client = axios.create({
    baseURL: "http://127.0.0.1:8000"
  });

  const navigate = useNavigate();

  const [openPicker, authResponse] = useDrivePicker(); 
  const [desc, setDesc] = useState(''); 
  const [title, setTitle] = useState(''); 
  const [subject, setSubject] = useState(''); 

  const handleOpenPicker = () => {
    openPicker({
      clientId: "1028915425652-6slsj5jr1d9ncfsccnkfo05ujccmav1f.apps.googleusercontent.com",
      developerKey: "AIzaSyBQGcUZhVxAMA5mvSObIsV41IpQjJlxcvo",
      viewId: "DOCS",
      showUploadView: true,
      showUploadFolders: true,
      supportDrives: true,
      multiselect: true,
      callbackFunction: (data) => {
        if (data.action === 'cancel') {
          console.log('User clicked cancel/close button');
        } else if (data.action === 'picked') {
          const body = {
            "title": title,
            "description": desc,
            "subject": subject,
            "url": data["docs"][0]["url"],
          };
          const headers = {
            "Content-Type": "application/json",
            "Authorization": "Token " + localStorage.getItem("token"),
          };
          console.log(body);
          client.post("/api/v1/upload-slides/", body, {
            headers: headers,
          }).then(res => {
            console.log(res.data);
            navigate("/resources");
          }).catch(err => {
            console.log(err);
          })
        }
        console.log(data);
      },
    })
  }

  return (
    <Container>
      <ContentWithPaddingXl>
        <HeaderContainer>
          {subheading && <Subheading>{subheading}</Subheading>}
          <Heading>{heading}</Heading>
          {description && <Description>{description}</Description>}

        {/* <PlanDurationSwitcher>
          {planDurations.map((planDuration, index) => (
            <SwitchButton active={activeDurationIndex === index} key={index} onClick={() => setActiveDurationIndex(index)}>{planDuration.switcherText}</SwitchButton>
          ))}
        </PlanDurationSwitcher> */}
        </HeaderContainer>
        <PlansContainer>
          <Input type="text" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)}/>
          <Input type="text" placeholder="Subject" value={subject} onChange={e => setSubject(e.target.value)}/>
          <LongInput type="text" placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)}/>
          <PlanAction>
            <BuyNowButton onClick={handleOpenPicker}>Upload Slides</BuyNowButton>
          </PlanAction>
          {/* {plans.map((plan, index) => (
            <Plan key={index} featured={plan.featured}>
              <PlanHeader>
                <span className="priceAndDuration">
                  <span className="price">{plan.durationPrices[activeDurationIndex]}</span>
                  <span className="slash"> / </span>
                  <span className="duration">{planDurations[activeDurationIndex].text}</span>
                </span>
                <span className="name">{plan.name}</span>
                <span className="mainFeature">{plan.mainFeature}</span>
              </PlanHeader>
              <PlanFeatures>
                {plan.features.map((feature, index) => (
                  <span key={index} className="feature">
                    {feature}
                  </span>
                ))}
              </PlanFeatures>
              <PlanAction>
                <BuyNowButton onClick={handleOpenPicker}>Upload Slides</BuyNowButton>
              </PlanAction>
            </Plan>
          ))} */}
        </PlansContainer>
      </ContentWithPaddingXl>
      <DecoratorBlob1 />
      <DecoratorBlob2 />
    </Container>
  );
};
