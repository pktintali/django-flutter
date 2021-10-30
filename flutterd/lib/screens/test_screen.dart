import 'package:flutter/material.dart';
import 'package:flutterd/models/miscard.dart';
import 'package:flutterd/state/miscard_state.dart';
import 'package:provider/provider.dart';

class TestScreen extends StatefulWidget {
  static final String routeName = 'test_screen';
  const TestScreen({Key key}) : super(key: key);

  @override
  State<TestScreen> createState() => _TestScreenState();
}

class _TestScreenState extends State<TestScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Column(
        children: [
          SizedBox(
            height: 400,
            child: FutureBuilder(
              future: Provider.of<MiscardState>(context, listen: false)
                  .getMisCards(),
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  print(snapshot.data);
                  List<MisCard> data =
                      Provider.of<MiscardState>(context, listen: false)
                          .miscards;
                  return ListView.builder(
                    itemCount: data.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        onTap: () {},
                        title: Text(data[index].title),
                      );
                    },
                  );
                }
                return Center(
                  child: CircularProgressIndicator(),
                );
              },
            ),
          ),
          Center(
            child: TextButton(
              child: Text('POST'),
              onPressed: () async {
                await Provider.of<MiscardState>(context, listen: false)
                    .testing();
                // .addMiscard('Patched Title', 'Mistake 4', 'Lesson 4',1)
                // .then((value) => setState(() {
                //       print(value);
                //     }));
              },
            ),
          )
        ],
      ),
    );
  }
}
