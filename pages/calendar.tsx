import React from "react";
import Link from "next/link";
import { Event } from "../lib/types";
import Markdown from "../components/Markdown";
import { AiOutlineClockCircle } from "react-icons/ai";

export async function getStaticProps() {
	//gets all events that are ending today or later and sorts them by date
	let today = new Date()
		.toLocaleDateString("en-GB")
		.split("/")
		.reverse()
		.join("-");
	let events = await fetch(
		`https://strapi.mbhs.edu/api/events?filters[endDate][$gte]=${today}&sort=startDate:ASC`
	).then((res) => res.json());

	return {
		props: {
			events: events.data,
		},
	};
}

interface CalendarProps {
	events: Event[];
}

const parseTime = (time: string) => {
	let timeArr = time.split(":");
	let hours = parseInt(timeArr[0]);
	let minutes = parseInt(timeArr[1]);
	let ampm = hours >= 12 ? "PM" : "AM";
	hours = hours % 12;
	if (hours == 0) {
		hours = 12;
	}
	return `${hours < 10 ? "0" + hours : hours}:${
		minutes < 10 ? "0" + minutes : minutes
	} ${ampm}`;
};

export default function Calendar({ events }: CalendarProps) {
	return (
		<div className="rounded-lg p-2 md:px-40">
			<h1 className="text-xl md:text-4xl font-bold text-center pb-3">
				Calendar
			</h1>
			<div className="flex flex-col gap-5 flex-wrap">
				{events.map(
					({ attributes: { title, description, startDate, startTime } }, i) => (
						<div
							className="rounded-lg bg-black bg-opacity-20 hover:bg-opacity-10 transition-all duration-300 backdrop-blur-md p-3 text-sm w-full break-words"
							key={i}
						>
							<div className="flex gap-3">
								<div className="flex flex-col justify-center items-center text-center font-semibold bg-red-600 text-white p-2 h-16 w-16 rounded-full">
									<p className="text-md -mb-1">
										{new Date(startDate).toLocaleString("default", {
											timeZone: "UTC",
											month: "short",
										})}
									</p>
									<p className="text-xl">
										{new Date(startDate).toLocaleString("default", {
											timeZone: "UTC",
											day: "numeric",
										})}
									</p>
								</div>

								<div className="flex-1">
									<p className="font-semibold text-lg">{title}</p>
									<p className="flex gap-1 items-center">
										<AiOutlineClockCircle /> {startTime && parseTime(startTime)}
									</p>
									<Markdown>{description}</Markdown>
								</div>
							</div>
						</div>
					)
				)}
			</div>
		</div>
	);
}
