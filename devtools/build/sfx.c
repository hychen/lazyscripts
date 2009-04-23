/*
 *      sfx.c: Creating self-extracting tar.gz for Lazybuntu
 *      
 *      Copyright 2007 Houng Jen Yee (PCMan) <pcman.tw@gmail.com>
 *      
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *      
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *      
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *      MA 02110-1301, USA.
 */


#include <stdio.h>
#include <glib.h>
#include <gtk/gtk.h>

#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

static GPid pid = -1;
static int std_in = -1;
static char *cmdv[]={ "tar", "xz", "-C", NULL, NULL };

static char magic[] = "XDATA_BEGIN_";
static const int magic_len = G_N_ELEMENTS( magic ) - 1;

void show_error( const char* msg )
{
    GtkWidget* dlg;
    dlg = gtk_message_dialog_new( NULL, 0, GTK_MESSAGE_ERROR, GTK_BUTTONS_OK, msg );
    gtk_dialog_run( (GtkDialog*)dlg );
    gtk_widget_destroy( dlg );    
}

int main(int argc, char** argv)
{
    GError *err = NULL;
    GMappedFile *map;
    char *buf = NULL, *pbuf = NULL, *data = NULL, *end;
    gsize len = 0;
    char *extract_path;

    gtk_init( &argc, &argv );

    /* load the executable file itself */
    map = g_mapped_file_new( argv[0], FALSE, NULL );
    if( !map )
        return 1;

    buf = g_mapped_file_get_contents(map);
    len = g_mapped_file_get_length( map );

    /* find the data */
    magic[0] = '_';

    for( pbuf = buf, end = buf + len - magic_len; G_LIKELY( pbuf < end ); ++pbuf )
    {
        if( G_UNLIKELY( 0 == memcmp( pbuf, magic, magic_len ) ) )
        {
            data = pbuf + magic_len + 1;
            break;
        }
    }

    if( G_UNLIKELY( ! data ) )
    {
        g_mapped_file_free( map );
        show_error( "檔案損毀，請重新下載。" );
        return 1;   /* error!  no data found */
    }

    len -= (data - buf);    /* skip ourself */

    extract_path = g_strconcat( "/tmp/lazyscripts-", g_get_user_name(), NULL );
    g_mkdir_with_parents( extract_path, 0755 ); /* FIXME: is 0755 OK? */

    cmdv[3] = extract_path;
    if(
        g_spawn_async_with_pipes
            ( NULL, cmdv, NULL, 
            G_SPAWN_SEARCH_PATH|G_SPAWN_DO_NOT_REAP_CHILD,
            NULL, NULL, &pid, &std_in, NULL, NULL, &err )
    )
    {
        int status = 0;
        write( std_in, data, len );
        close( std_in );
        waitpid( pid, &status, 0 );
        g_spawn_close_pid( pid );
    }
    else
    {
        show_error( err->message );   
        g_error_free( err );
    }
    g_mapped_file_free( map );

    g_chdir( extract_path );
    g_free( extract_path );
    g_chdir( "lazyscript" );
    execl ("slzs", "gui" );

    show_error("錯誤，無法執行 lazyscripts！");

    return 0;
}
