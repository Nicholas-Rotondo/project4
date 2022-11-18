from threading import Thread
import subprocess
import time
def rec_tester():
    port = 50007
    for _ in range(10):
    
        send_data = subprocess.run("python3 sender.py --port " + str(port), capture_output = True, shell = True)
        if(send_data.returncode != 0):
            errors = send_data.stderr.decode("utf-8")
            raise Exception( f'Invalid result in running: python3 sender.py --port {port}: { errors }' )
        
        time.sleep(.1)

def send_tester():
    commands = []
    commands.append(["python3 receiver.py --port ", " --pktloss noloss --ackloss noloss"])
    commands.append(["python3 receiver.py --port ", " --pktloss everyn --pktlossN 3 --ackloss noloss"])
    commands.append(["python3 receiver.py --port ", " --pktloss everyn --pktlossN 10 --ackloss noloss"])
    commands.append(["python3 receiver.py --port ", " --pktloss noloss --ackloss everyn --acklossN 3"])
    commands.append(["python3 receiver.py --port ", " --pktloss noloss --ackloss everyn --acklossN 10"])
    commands.append(["python3 receiver.py --port ", " --pktloss alteveryn --pktlossN 8 --ackloss noloss"])
    commands.append(["python3 receiver.py --port ", " --pktloss noloss --ackloss alteveryn --acklossN 8"])
    commands.append(["python3 receiver.py --port ", " --pktloss iid --pktlossN 5 --ackloss noloss"])
    commands.append(["python3 receiver.py --port ", " --pktloss noloss --ackloss iid --acklossN 5"])
    commands.append(["python3 receiver.py --port ", " --pktloss everyn --pktlossN 5 --ackloss alteveryn --acklossN 4"])

    port = 50007
    for comm in commands:
        command = comm[0] + str(port) + comm[1]
        print(f"trying command => {command}")
        rec_data = subprocess.run(command, capture_output = True, shell = True)
        
        
        if(rec_data.returncode != 0):
            errors = rec_data.stderr.decode("utf-8")
            raise Exception( f'Invalid result in running: {command}: { errors }' )
       
        diff_data = subprocess.run("diff test-input.txt test-output.txt", capture_output = True, shell = True)
        if(diff_data.returncode != 0):
            errors = diff_data.stderr.decode("utf-8")
            raise Exception( f'Invalid result in running diff: { errors }, output: {diff_data.stdout.decode("utf")}' )
        if(len(diff_data.stdout) != 0):
            result = diff_data.stdout.decode("utf-8")
            raise Exception( f'there was a difference: { result }' )
        else:
            print("diff says good!")
        f = open("test-output.txt", "w")
        f.close()
        time.sleep(.1)

if __name__ == "__main__":
    print("diff test:")
    f = open("test-output.txt", "w")
    f.close()
    diff_data = subprocess.run("diff test-input.txt test-output.txt", capture_output = True, shell = True)
    if(diff_data.returncode != 0 or len(diff_data.stdout) != 0):
        errors = diff_data.stderr.decode("utf-8")
        print( f'Invalid result in running diff: { errors }, output: {diff_data.stdout.decode("utf")}' )
        print("diff works!")

    t1 = Thread(target=rec_tester)
    t2 = Thread(target=send_tester)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
