namespace WindowsFormsApplication1
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.notifyIcon1 = new System.Windows.Forms.NotifyIcon(this.components);
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.playGameMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.shellToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.codeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.udkEditorMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.dToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.metricsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.furballToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.mayaToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.dCmdsStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.mkdataToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.syncToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.animProgToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.quitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.contextMenuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // notifyIcon1
            // 
            this.notifyIcon1.ContextMenuStrip = this.contextMenuStrip1;
            this.notifyIcon1.Icon = ((System.Drawing.Icon)(resources.GetObject("notifyIcon1.Icon")));
            this.notifyIcon1.Text = "Scrpayard Tray";
            this.notifyIcon1.Visible = true;
            this.notifyIcon1.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.notifyIcon1_MouseDoubleClick);
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.ImageScalingSize = new System.Drawing.Size(32, 32);
            this.contextMenuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
                this.playGameMenuItem,
                this.shellToolStripMenuItem,
                this.codeToolStripMenuItem,
                this.udkEditorMenuItem,
                this.dToolStripMenuItem,
                this.dCmdsStripMenuItem,
                this.quitToolStripMenuItem}
            );
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(120, 194);
            this.contextMenuStrip1.Text = "Scrapyard Launcher";
            // 
            // playGameMenuItem
            // 
            this.playGameMenuItem.Image = global::ScrapyardTray.Properties.Resources.playGame;
            this.playGameMenuItem.Name = "playGameMenuItem";
            this.playGameMenuItem.Size = new System.Drawing.Size(119, 38);
            this.playGameMenuItem.Text = "Play!";
            this.playGameMenuItem.Click += new System.EventHandler(this.playGameMenuItem_Click);// 
            // shellToolStripMenuItem
            // 
            this.shellToolStripMenuItem.Image = global::ScrapyardTray.Properties.Resources.cmd;
            this.shellToolStripMenuItem.Name = "shellToolStripMenuItem";
            this.shellToolStripMenuItem.Size = new System.Drawing.Size(119, 38);
            this.shellToolStripMenuItem.Text = "Shell";
            this.shellToolStripMenuItem.Click += new System.EventHandler(this.shellToolStripMenuItem_Click);
            // 
            // codeToolStripMenuItem
            // 
            this.codeToolStripMenuItem.Image = global::ScrapyardTray.Properties.Resources.dev;
            this.codeToolStripMenuItem.Name = "codeToolStripMenuItem";
            this.codeToolStripMenuItem.Size = new System.Drawing.Size(119, 38);
            this.codeToolStripMenuItem.Text = "Code";
            this.codeToolStripMenuItem.Click += new System.EventHandler(this.codeToolStripMenuItem_Click);
            // 
            // udkEditorMenuItem
            // 
            this.udkEditorMenuItem.Image = global::ScrapyardTray.Properties.Resources.udk;
            this.udkEditorMenuItem.Name = "udkEditorMenuItem";
            this.udkEditorMenuItem.Size = new System.Drawing.Size(119, 38);
            this.udkEditorMenuItem.Text = "UDK";
            this.udkEditorMenuItem.Click += new System.EventHandler(this.udkEditorMenuItem_Click);
            // 
            // dToolStripMenuItem
            // 
            this.dToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
                this.metricsToolStripMenuItem,
                this.furballToolStripMenuItem,
            this.mayaToolStripMenuItem});
            this.dToolStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("dToolStripMenuItem.Image")));
            this.dToolStripMenuItem.Name = "dToolStripMenuItem";
            this.dToolStripMenuItem.Size = new System.Drawing.Size(119, 38);
            this.dToolStripMenuItem.Text = "Tools";
            // 
            // metricsToolStripMenuItem
            // 
            this.metricsToolStripMenuItem.Name = "metricsToolStripMenuItem";
            this.metricsToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.metricsToolStripMenuItem.Text = "Metrics";
            this.metricsToolStripMenuItem.Click += new System.EventHandler(this.metricsToolStripMenuItem_Click);
            // 
            // furballToolStripMenuItem
            // 
            this.furballToolStripMenuItem.Image = global::ScrapyardTray.Properties.Resources.furball;
            this.furballToolStripMenuItem.Name = "furballToolStripMenuItem";
            this.furballToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.furballToolStripMenuItem.Text = "Furball";
            this.furballToolStripMenuItem.Click += new System.EventHandler(this.furballToolStripMenuItem_Click);
            // 
            // mayaToolStripMenuItem
            // 
            this.mayaToolStripMenuItem.Image = global::ScrapyardTray.Properties.Resources.maya;
            this.mayaToolStripMenuItem.Name = "mayaToolStripMenuItem";
            this.mayaToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.mayaToolStripMenuItem.Text = "Maya";
            this.mayaToolStripMenuItem.Click += new System.EventHandler(this.mayaToolStripMenuItem_Click);
            // 
            // dCmdsStripMenuItem
            // 
            this.dCmdsStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
                this.mkdataToolStripMenuItem,
                this.syncToolStripMenuItem,
                this.animProgToolStripMenuItem
            });
            this.dCmdsStripMenuItem.Image = ((System.Drawing.Image)(resources.GetObject("dCmdsStripMenuItem.Image")));
            this.dCmdsStripMenuItem.Name = "dCmdsStripMenuItem";
            this.dCmdsStripMenuItem.Size = new System.Drawing.Size(119, 38);
            this.dCmdsStripMenuItem.Text = "Commands";
            // 
            // mkdataToolStripMenuItem
            // 
            this.mkdataToolStripMenuItem.Image = global::ScrapyardTray.Properties.Resources.mkdata;
            this.mkdataToolStripMenuItem.Name = "mkdataToolStripMenuItem";
            this.mkdataToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.mkdataToolStripMenuItem.Text = "Build Data";
            this.mkdataToolStripMenuItem.Click += new System.EventHandler(this.mkdataToolStripMenuItem_Click);
            // 
            // syncToolStripMenuItem
            // 
            this.syncToolStripMenuItem.Image = global::ScrapyardTray.Properties.Resources.sync;
            this.syncToolStripMenuItem.Name = "syncToolStripMenuItem";
            this.syncToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.syncToolStripMenuItem.Text = "Cust Sync P4";
            this.syncToolStripMenuItem.Click += new System.EventHandler(this.syncToolStripMenuItem_Click);
            // 
            // animProgToolStripMenuItem
            // 
            this.animProgToolStripMenuItem.Image = global::ScrapyardTray.Properties.Resources.animProg;
            this.animProgToolStripMenuItem.Name = "animProgToolStripMenuItem";
            this.animProgToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.animProgToolStripMenuItem.Text = "Anim Prog";
            this.animProgToolStripMenuItem.Click += new System.EventHandler(this.animProgToolStripMenuItem_Click);
            // 
            // quitToolStripMenuItem
            // 
            this.quitToolStripMenuItem.Name = "quitToolStripMenuItem";
            this.quitToolStripMenuItem.Size = new System.Drawing.Size(119, 38);
            this.quitToolStripMenuItem.Text = "Quit";
            this.quitToolStripMenuItem.Click += new System.EventHandler(this.quitToolStripMenuItem_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(284, 262);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Name = "Form1";
            this.Opacity = 0;
            this.ShowInTaskbar = false;
            this.Text = "Form1";
            this.WindowState = System.Windows.Forms.FormWindowState.Minimized;
            this.contextMenuStrip1.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.NotifyIcon notifyIcon1;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.ToolStripMenuItem playGameMenuItem;
        private System.Windows.Forms.ToolStripMenuItem shellToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem codeToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem udkEditorMenuItem;
        private System.Windows.Forms.ToolStripMenuItem dToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem metricsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem mayaToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem furballToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem dCmdsStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem mkdataToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem syncToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem animProgToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem quitToolStripMenuItem;
    }
}

