echo "Expects compiler.jar (or symlink) in this folder"
echo "See https://developers.google.com/closure/compiler/docs/gettingstarted_app"
echo "--- compiling, please wait ... ---"
cd lib
java -jar ../compiler.jar \
--warning_level QUIET \
--js jquery.min.js \
--js jquery.color-2.1.2.min.js \
--js jquery.form.js \
--js jquery.placeholder.js \
--js bootstrap.min.js \
--js bootstrap-dialog.js \
--js leaflet.js \
--js leaflet.markercluster.js \
--js_output_file all.min.js
