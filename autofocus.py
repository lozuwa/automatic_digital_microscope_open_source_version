import z_positioner as zz
import vision as vis 
import algorithms as alg
import numpy as np
import time, os, sys 
import db as DB 

def autofocus_v3_debug(c):
 zz.activate_control_loop()

 print("Reset z")
 zz.z_reset()

 print("Analysis")
 samples = []
 img = []
 for i in range(25):
  frame = vis.take_picture()
  vis.show_picture(frame)

  img.append(frame)
  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=True)
  samples.append(frame_var)

  zz.z_up()
  print(frame_var, i)

 m = max(samples)
 index = samples.index(m)
 print("Start focus")
 print("Max: ", m, "Index: ", index)

 refocus = []
 count = 0
 while(True):
  frame = vis.take_picture()
  vis.show_picture(frame)

  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=True)
  refocus.append(frame_var)

  print(frame_var, count, (frame_var-m)**2)
  count+=1
  if ((40+40*1.5)-count < 0):
   break

  if (frame_var > m) or ( (frame_var-m)**2 < 0.5 ):
   print('done! ', frame_var, m)
   break
  elif ( (frame_var-m)**2 >= 0.5 and (frame_var-m)**2 < 2 ):
   print('mid focus')
   zz.z_mid_down()
   time.sleep(0.5)
  elif ( (frame_var-m)**2 >= 1 ) : 
  #elif ( (frame_var-m)**2 >= 1 and (frame_var-m)**2 < 10 ):
   print('normal focus')
   zz.z_down()
   time.sleep(0.5)
  else:
   pass 

 zz.deactivate_control_loop()

 #while(True):
 for i in range(20):
  frame = vis.take_picture()
  vis.show_picture(frame)
  vis.debug("Image in sequence max", img[index])

 # Save data
 vis.save_image(frame, c)
 #DB.insert_image(c)
 #DB.insert_value(c)
 #DB.update(c, samples, refocus)

 vis.exit()

def autofocus_v1(c):
 zz.activate_control_loop()

 print("Reset z")
 zz.z_reset()

 print("Analysis")
 samples = []
 img = []
 for i in range(45):
  frame = vis.take_picture()
  vis.show_picture(frame)

  img.append(frame)
  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=True)
  samples.append(frame_var)

  zz.z_up()
  print(frame_var, i)

 m = max(samples)
 index = samples.index(m)
 print("Start focus")
 print("Max: ", m, "Index: ", index)

 refocus = []
 count = 0
 while(True):
  frame = vis.take_picture()
  vis.show_picture(frame)

  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=True)
  refocus.append(frame_var)

  print(frame_var, count, (frame_var-m)**2)
  count+=1
  if ((40+40*1.5)-count < 0):
   break

  if (frame_var > m) or ( (frame_var-m)**2 < 0.5 ):
   print('done! ', frame_var, m)
   break
  elif ( (frame_var-m)**2 >= 0.5 and (frame_var-m)**2 < 1 ):
   print('fine focus')
   zz.z_fine_down()
  elif ( (frame_var-m)**2 >= 1 and (frame_var-m)**2 < 2 ):
   print('mid focus')
   zz.z_mid_down()
  else:
   print('macro focus')
   zz.z_down()

 zz.deactivate_control_loop()

 #while(True):
 for i in range(1):
  frame = vis.take_picture()
  vis.show_picture(frame)
  #vis.debug("Image in sequence max", img[index])

 # Save data
 vis.save_image(frame, c)
 DB.inser_image(c)
 DB.insert_value(c)
 DB.update(c, samples, refocus)

 vis.exit()

""" ------------------ FAILED TESTS ------------------------ """

def autofocus_v0():
 zz.activate_control_loop()

 # Z positioner has been already reseted?
 print('Reset z')
 zz.z_reset() 

 # ---------------------------AUTOFOCUS SEQUENCE----------------------------
 # Store fields for analysis
 print('Analysis')
 mic_fields = []
 img = []
 for i in range(30):
  frame = vis.take_picture()
  vis.show_picture(frame)
  
  img.append(frame)
  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
  mic_fields.append(frame_var)
  
  zz.z_up()
  
  print(frame_var, i)

 
 # Analyse fields 
 m = max(mic_fields)
 index = mic_fields.index(m)
 print('Focus point at: ', 30-index, 'Coordinates: ', index, ',', m)

 for i in range(np.abs(30-index)):
  frame = vis.take_picture()
  vis.show_picture(frame)

  frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)

  zz.z_down()

  print(frame_var, i)

 zz.deactivate_control_loop()

 print('Focused point ')
 while(1):
  frame = vis.take_picture()
  vis.show_picture(frame)
  vis.debug('Stored_image', img[index])

def autofocus_v2():
 zz.activate_control_loop()

 # Z positioner has been already reseted?
 print('Reset')
 zz.z_reset()

 # --------------------- Macroscopic focus ------------------------
 print('Macroscopic focus')
 chunks = [20, 8, 4]
 biases = [4, 2, 1]
 for c, b in zip(chunks, biases):
  # Store data
  mic_fields = []
  for i in range(int(c)):

   frame = vis.take_picture()
   vis.show_picture(frame)

   frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
   mic_fields.append((frame_var, i))
   print(i, frame_var)
        
   zz.activate_control_loop()
   zz.z_up()
   zz.deactivate_control_loop()

  # Analyse data
  r_ = alg.get_max(mic_fields)
  zeroed_position = (c - r_[1])
  for i in range(zeroed_position + b):
   zz.activate_control_loop()
   zz.z_down()
   zz.deactivate_control_loop()
 
 # ------------------------ Fine focus ---------------------------
 print('Fine focus')
 zz.activate_control_loop()
 chunks = [10, 4, 2]
 biases = [2, 1, 0]
 for c, b in zip(chunks, biases):
  # Store data
  mic_fields = []
  for i in range(int(c)):
   frame = vis.take_picture()
   vis.show_picture(frame)
   
   frame, frame_var = vis.laplacian(frame, debug=True, gaussian=False)
   mic_fields.append((frame_var, i))
   
   #zz.activate_control_loop()
   zz.z_fine_up()
   #zz.deactivate_control_loop()

  # Analyse data
  r_ = alg.get_max(mic_fields)
  zeroed_positioner = (c - r_[1])
  for i in range(zeroed_position + b):
   #zz.activate_control_loop()
   zz.z_fine_down()
   #zz.deactivate_control_loop()

 zz.deactivate_control_loop()

 print('Focused point ')
 while(1):
  frame = vis.take_picture()
  vis.show_picture(frame)
  #vis.debug('Stored_image', img[r_[1]])

def exit():
 vis.cap.release()
 zz.ser.close()
 vis.cv2.destroyAllWindows()

if __name__ == '__main__':
 autofocus_v1()
