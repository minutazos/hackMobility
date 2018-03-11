import asyncio
import cozmo

def do_lookforface(robot):
	for i in range(5):
		robot.say_text(str(i + 1)).wait_for_completed()
	any_face = None
	print("Looking for a face...")
	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
	robot.move_lift(-3)
	look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)

	try:
		any_face = robot.world.wait_for_observed_face(timeout=15)

	except asyncio.TimeoutError:
		print("Didn't find anyone :-(")


	finally:
		# whether we find it or not, we want to stop the behavior
		look_around.stop()

	if any_face is None:
		robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
		robot.say_text("Okei, You win").wait_for_completed()
		return

	print("Yay, found someone!")
	robot.play_anim_trigger(cozmo.anim.Triggers.ReactToBlockPickupSuccess).wait_for_completed()
	robot.say_text("I found you").wait_for_completed()


cozmo.run_program(do_lookforface,use_viewer=True, force_viewer_on_top=True)
