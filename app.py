"""This module contains functions for getting youtube data."""


import contextlib
import traceback
import requests
# import Iterable
from typing import List

import streamlit as st
from concurrent.futures import ThreadPoolExecutor
PING_TIMEOUT_TIME = 0.4


def get_urls(urls, timeout=PING_TIMEOUT_TIME):
    """Returns a list of responses from the given urls."""
    with contextlib.ExitStack() as stack:
        sessions = [stack.enter_context(requests.Session()) for _ in urls]
        for session in sessions:
            session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
            session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
        responses = [
            session.get(url, timeout=timeout) for session, url in zip(sessions, urls)
        ]
    return responses


def get_live_urls(urls, timeout=PING_TIMEOUT_TIME):
    """Returns the live urls."""
    try:
        instances = []
        responses = get_urls(urls, timeout=timeout)
        for response, url in zip(responses, urls):
            if response.ok:
                url = response.history[0].url if response.history else response.url
                # remove the trailing slash
                if url.endswith("/"):
                    url = url[:-1]
                instances_with_elapsedtime = (url, response.elapsed.total_seconds())
                instances.append(instances_with_elapsedtime)
        instances.sort(key=lambda x: x[1])

        return [instance[0] for instance in instances]

    except Exception as error:  # pylint: disable=broad-except
        print(error)
        traceback.print_exc()
        return get_live_urls(urls, timeout=timeout * 2)



def get_invidious_instances_from_json():
    """scrape domain instances from my URl"""
    url = "https://api.invidious.io/instances.json?pretty=1&sort_by=type,users"
    response = requests.get(url)
    instances = []
    instances_api = []
    if response.ok:

        data = response.json()
        for instance in data:
            type_of_instance = instance[1]["type"]
            url = instance[1]["uri"]

            if type_of_instance == "https":
                instances.append(url)
                api = instance[1]["api"]
                if api:
                    instances_api.append(url)
    else:
        # print_status_and_text_from_response(response)
        print("Error getting invidious instances from json")
        print(response.text)


    live_instances = get_live_urls(instances)
    live_instances_api = get_live_urls(instances_api)

    return live_instances, live_instances_api


try:

    invidious_instances, invidious_instances_api = get_invidious_instances_from_json()

except Exception as e:  # pylint: disable=broad-except
    print(e)
    traceback.print_exc()

def return_de_duped_list(list_):
    """Returns a list with no duplicates."""
    return list(set(list_))


def return_video_ids_from_playlist_id_from_invidious(
    playlist_id: str,
) -> List[str]:
    """Returns a list of video ids from a playlist id."""
    for instance in invidious_instances_api:
        urls = [
            f"{instance}/api/v1/playlists/{playlist_id}?page={page}"
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
                print(error)
                print(response.text)
                continue
            return video_ids


def info_from_video_id_from_invidious_api(video_id):
    """Returns the info of a video from its video id."""
    try:
        for instance in invidious_instances_api:
            api_instance = instance
            url = f"{api_instance}/api/v1/videos/{video_id}"
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
                video_infos = executor.map(info_from_video_id_from_invidious_api, video_ids)


        # get the length of the videos
        video_lengths = [video_info["lengthSeconds"] for video_info in video_infos]

        # get the total length of the playlist
        total_length = sum(video_lengths)

        # convert the total length to hours, minutes and seconds
        hours, remainder = divmod(total_length, 3600)
        minutes, seconds = divmod(remainder, 60)

        # display the total length
        st.write(f"Total length of the playlist is {hours} hours {minutes} minutes {seconds} seconds")

        # write the length of each video
        for video_info, video_length in zip(video_infos, video_lengths):
            hours, remainder = divmod(video_length, 3600)
            minutes, seconds = divmod(remainder, 60)
            st.write(f"{video_info['title']} is {hours} hours {minutes} minutes {seconds} seconds")
