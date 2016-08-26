using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System;
using System.IO;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void quitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void playGameMenuItem_Click(object sender, EventArgs e)
        {
            //Create process
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Binaries/Win32/UDK.exe";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "CharacterHangar_4player?game=Scrapyard -nomoviestartup -log -ConsolePosX=0 -ConsolePosY=0";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Optional
            //pProcess.StartInfo.WorkingDirectory = Directory.GetCurrentDirectory();

            //Start the process
            pProcess.Start();

            //Get program output
            //string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            //pProcess.WaitForExit();
        }

        private void codeToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create process
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            ;
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Development/Src/Scrapyard.sln";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Optional
            //pProcess.StartInfo.WorkingDirectory = Directory.GetCurrentDirectory();

            //Start the process
            pProcess.Start();

            //Get program output
            //string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            //pProcess.WaitForExit();
        }

        private void shellToolStripMenuItem_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();


            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/SYShell.bat";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Optional
            pProcess.StartInfo.WorkingDirectory = Directory.GetCurrentDirectory();

            //Start the process
            pProcess.Start();
        }

        private void udkEditorMenuItem_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();


            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Binaries/Win32/UDK.exe";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "editor -log";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Optional
            //pProcess.StartInfo.WorkingDirectory = Directory.GetCurrentDirectory() + "/..";

            //Start the process
            pProcess.Start();

        }

        private void furballToolStripMenuItem_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            ;
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/FurBall.bat";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Optional
            //pProcess.StartInfo.WorkingDirectory = Directory.GetCurrentDirectory() + "/..";

            //Start the process
            pProcess.Start();
        }

        private void mayaToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create process
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            ;
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Tools/maya/maya.bat";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Optional
            //pProcess.StartInfo.WorkingDirectory = Directory.GetCurrentDirectory() + "/..";

            //Start the process
            pProcess.Start();

            //Get program output
            //string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            //pProcess.WaitForExit();
        }

        private void metricsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create process
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            ;
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Tools/Java/Scrapyard Metrics Grapher/Scrapyard Metrics Grapher.jar";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Start the process
            pProcess.Start();

            //Get program output
            //string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
           // pProcess.WaitForExit();
        }

        private void mkdataToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create process
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            ;
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Tools/ShellCommands/mkdata.bat";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Start the process
            pProcess.Start();

            //Get program output
            //string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            // pProcess.WaitForExit();
        }

        private void syncToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create process
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            ;
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Tools/ShellCommands/sync.bat";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Start the process
            pProcess.Start();

            //Get program output
            //string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            // pProcess.WaitForExit();
        }

        private void animProgToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create process
            System.Diagnostics.Process pProcess = new System.Diagnostics.Process();

            //strCommand is path and file name of command to run
            ;
            pProcess.StartInfo.FileName = Directory.GetCurrentDirectory() + "/Tools/ShellCommands/animProg.bat";

            //strCommandParameters are parameters to pass to program
            pProcess.StartInfo.Arguments = "";

            pProcess.StartInfo.UseShellExecute = true;

            //Set output of program to be written to process output stream
            pProcess.StartInfo.RedirectStandardOutput = false;

            //Start the process
            pProcess.Start();

            //Get program output
            //string strOutput = pProcess.StandardOutput.ReadToEnd();

            //Wait for process to finish
            // pProcess.WaitForExit();
        }

        private void notifyIcon1_MouseDoubleClick(object sender, MouseEventArgs e)
        {

        }
    }
}
