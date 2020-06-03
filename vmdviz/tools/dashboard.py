import matplotlib.pyplot as plt
import numpy as np
import cv2

class Dashboard():
    """Class for organizing and displaying movies in a single window

    Parameters
    ----------
    movie_list : list of movie files
        List of movie files. THe order of the list detemines the order
        of the movies in the display window
    labels : list of str (default=None)
        List of string labels for each movie in the display frame,
        running in the same order as movie_list
    """

    def __init__(self, movie_files, labels=None):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.movie_list = [self.load_movie(name) for name in movie_files]
        self.current_indices = [0 for _ in self.movie_list]
        self.num_frames = [movie.get(cv2.CAP_PROP_FRAME_COUNT)
                           for movie in self.movie_list]
        if labels == None:
            self.labels = len(self.movie_list) * [""]
        else:
            self.labels = labels
        self.frames = [None for _ in self.movie_list]
        self.set_framesize()


    def load_movie(self, movie_file):
        """Load method using OpenCV"""
        return cv2.VideoCapture(movie_file)


    def reset_movies(self):
        """Method that resets all movies in self.movie_list
        to their zeroth frames
        """
        for num, movie in enumerate(self.movie_list):
            self.current_indices[num] = 0
            movie.set(cv2.CAP_PROP_POS_FRAMES, 0)


    def set_movies(self, frame_idx):
        """Method for setting the global frame index for all
        movies in self.movie_list

        Parameters
        ----------
        frame_idx : int
            the desired global frame index to set all movies in self.movie_list
            to
        """
        for num, (movie, current_idx, num_frames) in enumerate(zip(self.movie_list,
                            self.current_indices, self.num_frames)):
            if frame_idx < num_frames - 1 and frame_idx > 0:
                self.current_indices[num] = frame_idx
                movie.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)


    def release_movies(self):
        """Method that releases all movies in self.movie_list"""
        for movie in self.movie_list:
            movie.release()


    def read_frames(self):
        """Method for reading frames for all videos and returning
        read statuses/valid frames.

        Returns
        -------
        statuses : list of bool
            Read statuses for each movie in self.movie_list
        """
        statuses = [False for _ in self.movie_list]

        for num, (movie, current_idx, num_frames) in enumerate(zip(self.movie_list,
                            self.current_indices, self.num_frames)):
            if current_idx < num_frames - 1:
                self.current_indices[num] += 1
                status, frame = movie.read()
                statuses[num] = status
                if status:
                    self.frames[num] = frame
            else:
                statuses[num] = False
        return statuses


    def set_framesize(self):
        statuses = [False for _ in self.movie_list]

        for num, (movie, current_idx, num_frames) in enumerate(zip(self.movie_list,
                            self.current_indices, self.num_frames)):
            status, frame = movie.read()
            if status:
                self.frames[num] = frame
            else:
                statuses[num] = False
        final = cv2.hconcat(self.frames)

        # Due to openCV framesize conventions, the x-y dimensions
        # must be swapped
        self.window_size = (final.shape[:-1][1], final.shape[:-1][0])


    def display_frames(self, write=None):
        """Method for displaying individual frames for each movie in
        self.movie_list within a single window
        """
        for text, frame in zip(self.labels, self.frames):
            cv2.putText(frame, text, (100,50), self.font,
                        1, (255, 255, 255), 1)
        final = cv2.hconcat(self.frames)
        cv2.imshow('Frame', final)
        if write:
            write.write(final)


    def play_movies(self):
        """Method that loops all movies together in a single window.
        By default, the window resets after the longest movie finishes,
        while any shorter videos will simply remain at ther final frame.
        The window playback can be controlled using the following key
        commands below.

        Keyboard Controls
        -----------------
        'r' : Resets all videos to their first frames
        'q' : Ends video playback, releases all videos, and kills the
              playback window
        'p' : Pause all videos at their current frames. While in this
              mode, the user can key 'h' and 'l' to advance all video
              frames backward and forward respectively by a single frame.
        """

        cv2.startWindowThread()
        self.reset_movies()
        movie_key = None
        while(np.all([movie.isOpened() for movie in self.movie_list])):
            statuses = self.read_frames()
            if np.any(statuses):
                self.display_frames()
                movie_key = cv2.waitKey(1) & 0xFF

                # Quit catch
                if movie_key == ord('q'):
                    self.release_movies()
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                    break

                # Restart catch
                if movie_key == ord('r'):
                    self.reset_movies()
                    continue

                # Pause loop
                if movie_key == ord('p'):
                    movie_key = None
                    while(movie_key != ord('p')):
                        movie_key = cv2.waitKey(1) & 0xFF
                        # Reverse single frame
                        if movie_key == ord('h'):
                            new_index = max(self.current_indices) - 2
                            self.set_movies(new_index)
                            statuses = self.read_frames()
                            self.display_frames()
                            movie_key = None
                        if movie_key == ord('l'):
                            new_index = max(self.current_indices)
                            self.set_movies(new_index)
                            statuses = self.read_frames()
                            self.display_frames()
                            movie_key = None

            else:
                self.reset_movies()
                movie_key = None
                statuses = [False for _ in self.movie_list]
                continue


    def write_movie(self, filename, fourcc='MJPG'):
        """Method for writing combined movies to file"""
        cv2.startWindowThread()
        print("Creating and exporting movie to file...")
        outfile = cv2.VideoWriter(filename, 0,
                                  fourcc=cv2.VideoWriter_fourcc(*fourcc),
                                  fps=30, frameSize=self.window_size)
        self.reset_movies()
        movie_key = None
        if outfile.isOpened():
            while(np.all([movie.isOpened() for movie in self.movie_list])):
                statuses = self.read_frames()
                if np.any(statuses):
                    self.display_frames(write=outfile)
                else:
                    self.release_movies()
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                    break
            outfile.release()
        else:
            raise RuntimeError("outfile could not be opened.")
