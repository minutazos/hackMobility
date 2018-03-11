#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Hello World

Make Cozmo say 'Hello World' in this simple Cozmo SDK example program.
'''


import cozmo


def happy(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.PeekABooGetOutHappy ).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.BuildPyramidSuccess).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.BuildPyramidThankUser).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.BuildPyramidThankUser).wait_for_completed()

def exited(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabExcited).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabFireTruck).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()


def sad(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.TurtleRoll).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.DriveEndAngry).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.DriveLoopAngry).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.PeekABooGetOutSad).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabBored).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.NeedsMildLowEnergyRequest).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.Shocked).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.Surprise).wait_for_completed()

def sleep(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.Sleeping).wait_for_completed()

def sing(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.Singing_120bpm).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.Singing_GetOut).wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.Singing_GetIn).wait_for_completed()

def sneeze(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabSneeze).wait_for_completed()

cozmo.run_program(happy)
