"""This module contains functions for getting youtube data."""

import contextlib
from concurrent.futures import ThreadPoolExecutor

# import Iterable
from typing import List

import requests
import streamlit as st

PING_TIMEOUT_TIME = 0.4

def get_urls(urls, timeout=10):
    """Returns a list of responses from the given urls."""
    with ThreadPoolExecutor(max_workers=1000) as executor:
        with contextlib.suppress(Exception):
            responses = executor.map(
                lambda url: requests.get(url, timeout=timeout), urls
            )
            return responses


def return_de_duped_list(list_):
    """Returns a list with no duplicates."""
    return list(set(list_))

def return_video_ids_from_playlist_id_from_invidious(
    playlist_id: str,
) -> List[str]:
    """Returns a list of video ids from a playlist id."""
    urls = [
        f"https://vid.puffyan.us//api/v1/playlists/{playlist_id}?page={page}"
        for page in range(1, 2)
    ]
    urls = return_de_duped_list(urls)
    responses = get_urls(urls)
    video_ids = []
    for response in responses:
        if not response.ok:
            print(response.text)

            continue
        try:
            data = response.json()
            videos = data["videos"]
            video_ids.extend(video["videoId"] for video in videos)
        except Exception as error:  # pylint: disable=broad-except
            print(
                "function return_video_ids_from_playlist_id_from_invidious have error",
                error,
            )
            print(response.text)
            continue
        return video_ids

def info_from_video_id_from_invidious_api(video_id):
    """Returns the info of a video from its video id."""
    try:
        url = f"https://vid.puffyan.us//api/v1/videos/{video_id}"
        response = requests.get(url, timeout=10)

        if response.ok:
            response = response.json()
            return response
        if response.status_code == 500:
            return None

    except Exception as error:  # pylint: disable=broad-except

        print("function info_from_video_id_from_invidious_api.")
        print(error)


def main():
    """we are making a streamlit app that can tell the complete length of a playlist"""

    # give title to the app
    st.title("Playlist Length Calculator")

    # give a description to the app
    st.write("This app will tell you the complete length of a playlist")

    # give a label to the input box
    playlist_link = st.text_input("Enter the playlist link")

    # give a label to the button
    if st.button("Calculate"):

        # get the playlist id from the link
        playlist_id = playlist_link.split("list=")[1]

        # get the video ids from the playlist id
        video_ids = return_video_ids_from_playlist_id_from_invidious(playlist_id)

        # # get the info of the videos from the video ids concurrently
        # video_infos = [info_from_video_id_from_invidious_api(video_id) for video_id in video_ids]

        with st.spinner("Calculating..."):
            with ThreadPoolExecutor(max_workers=10) as executor:
                video_infos = executor.map(
                    info_from_video_id_from_invidious_api, video_ids
                )

        # get the length of the videos
        video_lengths = []
        for video_info in video_infos:
            try:
                video_lengths.append(video_info["lengthSeconds"])
            except TypeError:
                continue
            except Exception as error:
                print(error)
                continue

        # get the total length of the playlist
        total_length = sum(video_lengths)

        # convert the total length to hours, minutes and seconds
        hours, remainder = divmod(total_length, 3600)
        minutes, seconds = divmod(remainder, 60)

        # display the total length
        st.write(
            f"Total length of the playlist is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 1.5x speed, 2x speed, 2.5x speed, 3x speed, 3.5x speed, 4x speed, 4.5x speed, 5x speed, 5.5x speed, 6x speed, 6.5x speed, 7x speed, 7.5x speed, 8x speed, 8.5x speed, 9x speed, 9.5x speed, 10x speed

        # write length of playlist if the video is seen at 1.5x speed
        one_point_five_x_speed = [
            int(video_length / 1.5) for video_length in video_lengths
        ]
        hours, remainder = divmod(sum(one_point_five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 1.5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 2x speed
        two_x_speed = [int(video_length / 2) for video_length in video_lengths]
        hours, remainder = divmod(sum(two_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 2x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 2.5x speed
        two_point_five_x_speed = [
            int(video_length / 2.5) for video_length in video_lengths
        ]
        hours, remainder = divmod(sum(two_point_five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 2.5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 3x speed
        three_x_speed = [int(video_length / 3) for video_length in video_lengths]
        hours, remainder = divmod(sum(three_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 3x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 3.5x speed
        three_point_five_x_speed = [
            int(video_length / 3.5) for video_length in video_lengths
        ]
        hours, remainder = divmod(sum(three_point_five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 3.5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 4x speed
        four_x_speed = [int(video_length / 4) for video_length in video_lengths]
        hours, remainder = divmod(sum(four_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 4x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 4.5x speed
        four_point_five_x_speed = [
            int(video_length / 4.5) for video_length in video_lengths
        ]
        hours, remainder = divmod(sum(four_point_five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 4.5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 5x speed
        five_x_speed = [int(video_length / 5) for video_length in video_lengths]
        hours, remainder = divmod(sum(five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)

        st.write(
            f"Total length of the playlist if the video is seen at 5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 5.5x speed
        five_point_five_x_speed = [
            int(video_length / 5.5) for video_length in video_lengths
        ]
        hours, remainder = divmod(sum(five_point_five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 5.5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 6x speed
        six_x_speed = [int(video_length / 6) for video_length in video_lengths]
        hours, remainder = divmod(sum(six_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 6x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 6.5x speed
        six_point_five_x_speed = [
            int(video_length / 6.5) for video_length in video_lengths
        ]
        hours, remainder = divmod(sum(six_point_five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 6.5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 7x speed
        seven_x_speed = [int(video_length / 7) for video_length in video_lengths]
        hours, remainder = divmod(sum(seven_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 7x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 7.5x speed
        seven_point_five_x_speed = [
            int(video_length / 7.5) for video_length in video_lengths
        ]
        hours, remainder = divmod(sum(seven_point_five_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 7.5x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write length of playlist if the video is seen at 8x speed
        eight_x_speed = [int(video_length / 8) for video_length in video_lengths]
        hours, remainder = divmod(sum(eight_x_speed), 3600)
        minutes, seconds = divmod(remainder, 60)
        st.write(
            f"Total length of the playlist if the video is seen at 8x speed is {hours} hours {minutes} minutes {seconds} seconds"
        )

        # write the length of each video
        for video_info, video_length in zip(video_infos, video_lengths):
            hours, remainder = divmod(video_length, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.write(
                f"{video_info['title']} is {hours} hours {minutes} minutes {seconds} seconds"
            )


if __name__ == "__main__":
    main()
